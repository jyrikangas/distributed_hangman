import asyncio
import json
import time
import os
import random
import socket
from dotenv import load_dotenv


from backend.elect_leader import Decisions
from objects.player import Player
load_dotenv()

OTHER_NODES = []
tasks = []
game = None
playerstates = {}
playerrolls = {}
host = ""
def logger(message):
    with open("log.txt", "a") as file:
        file.write(f'{time.time()}:{message}')

async def state(target=OTHER_NODES):
    await send_info({'Command':'State', 'State': game.as_JSON()}, target)

async def players():
    info = game.get_players()
    await send_info({'Players': info})

async def guess(letter):
    await send_info({'Command':'Guess','Letter': letter})

async def send_info(information, target=OTHER_NODES):
    print(len(OTHER_NODES))
    information.update({'from_ip': host, "from_name": game.playersbyaddress[host].name})
    print(information)
    for node in target:
        print(f"sending to {node.get_extra_info('peername')}")
        data = json.dumps(information)
        node[1].write(f'{data}\n'.encode())
        await node[1].drain()
        addr = node[1].get_extra_info('peername')
        logger(f'Message out {information} to {addr}')
        #response = await node[0].readline()
        #print(response.decode())


async def listen_for_connections(host, port):
    server = await asyncio.start_server(handle_client, host, port)
    print(f"Listening for connections on {host}:{port}")
    async with server:
        await server.serve_forever()

async def handle_client(reader, writer):

    while True:
        response = await reader.readline()
        decoded_json = response.decode()
        logger(f'Message in {decoded_json}')
        print("decoded_json:", decoded_json)
        decoded = json.loads(decoded_json)
        
        if decoded["from_ip"] not in game.playersbyaddress:
            new_player = Player(decoded["from_ip"])
            new_player.name = decoded["from_name"]
            game.add_player(new_player)
            
        if "Guess" == decoded["Command"]:
            game.guess_letter(decoded["Letter"])
            await send_info({'Command':'Response OK'})

        if "Response OK" == decoded["Command"]:
            print("OK")

        if "State" == decoded["Command"]:
            print("State")
            names = []
            sender = writer.get_extra_info('peername')
            message = decoded["State"]
            print(game)
            for player in game.get_players():
                names.append(player.name)
            for player in message["players"]:
                if player["name"] not in names:
                    new_player = Player(player["ip"])
                    new_player.create_name(game)
                    game.add_player(new_player)
                    await initiate_connection(player["ip"])
            for letter in message["guessed_letters"]:
                game.guess_letter(letter)

        if "Connect" == decoded["Command"]:
            OTHER_NODES.append((reader, writer))
            addr = writer.get_extra_info('peername')
            print(f"Connection from {addr}")
            #new_player = Player(addr[0])
            #new_player.create_name(game)
            
            #game.add_player(new_player)
            await state([(reader,writer)])

        if "Election" == decoded["Command"]:
            print("Election")
            addr = writer.get_extra_info('peername')
            logger(f"received election from {addr}")
        
        if "Ready" == decoded["Command"]:
            print("Ready received")
            name = decoded["from_name"]
            print(f"{name} is Ready")
            logger(f"{name} is Ready")
            playerstates[name] = True
            print(playerstates)
        
        if "ElectionRoll" == decoded["Command"]:
            print("ElectionRoll")
            roll = decoded["roll"]
            addr = writer.get_extra_info('peername')
            name = decoded["from_name"]
            print(f"{addr} name {name} rolled {roll}")
            logger(f"{addr} name {name} rolled {roll}")
            
            playerrolls[name] = roll
        
        if "TurnOrder" == decoded["Command"]:
            print("TurnOrder")
            received_turnorder = decoded["turnorder"]
            print(f"received {received_turnorder}, current {game.turnorder}")
            if received_turnorder !=game.turnorder:
                print("!!CONFLICT!!")
                game.turnorder = received_turnorder

            addr = writer.get_extra_info('peername')
            print(f"Turn order received from {addr}")
            logger(f"Turn order received from {addr}")
            print(game.turnorder)
            break
            
    

async def initiate_connection(target_host, target_port = "1999"):
    ourname = game.playersbyaddress[host].name
    try:
        theirname = game.playersbyaddress[target_host].name
    except:
        theirname = "Unknown"
    
    if ourname == theirname:
        logger(f"Tried to connect to self! \n")
        return
    try:
        print(f"Connecting to {target_host}:{target_port}")
        logger(f"Connecting to {target_host}:{target_port}")
        reader, writer = await asyncio.open_connection(target_host, target_port)
        print(f"Connected to {target_host}:{target_port}")
        
        await send_info({'Command': 'Connect'}, [(reader, writer)])
        OTHER_NODES.append((reader, writer))
        tasks.append(asyncio.create_task(handle_client(reader, writer)))
        

    except Exception as e:
        print(f"Failed to connect: {e}")


async def decide_order(game):
    #send message to all players to elect leader
    print("Deciding order")
    await send_info({'Command': 'Election'})
    
    #await ready
    print("awaiting ready")
    while True:
        print(playerstates)
        await asyncio.sleep(3)
        await send_info({'Command': 'Ready'})
        if len(playerstates) == len(game.players)-1:
            print("all players ready")
            break
    
    #after all players are ready, or 30 s have passed, start
    randomint = random.randint(1, 10000)
    playerrolls[game.playersbyaddress[host].name] = randomint
    
        
    #send random number between 1 and 10000
    print(f"sending random number {randomint}")
    await send_info({'Command': 'ElectionRoll', 'roll': randomint})
    
    #check who has the largest number
    await asyncio.sleep(1)
    while True:
        await asyncio.sleep(1)
        print(playerrolls)
        print(game.players)
        if len(playerrolls) == len(game.players):
            print("all players have rolled")
            break
    print(playerrolls)
    sort = sorted(playerrolls.items(), key=lambda x: x[1], reverse=True)
    print(sort)
    print()
    game.turnorder = [player[0] for player in sort]
    #tiebreaker based on ip
    #send turn order to all players
    print("sending turn order")
    await send_info({'Command': 'TurnOrder', 'turnorder': game.turnorder})
    print("turn order sent")

async def get_local_ip_async(target_host='8.8.8.8', target_port=80):
    loop = asyncio.get_running_loop()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        await loop.run_in_executor(None, s.connect, (target_host, target_port))
        local_ip = s.getsockname()[0]
    return local_ip

async def main(gameinst):
    global game
    global host
    game = gameinst
    host = await get_local_ip_async()
    port = 1999
    print(game.as_JSON())
    host_player = Player(host)
    host_player.create_name(game)
    game.add_player(host_player)
    
    try:
        await listen_for_connections("0.0.0.0", port, *tasks)
    except Exception as e:
        print(f"Failed to listen: {e}")

        await listen_for_connections("0.0.0.0", port, *tasks)
    

