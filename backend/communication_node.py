import asyncio
import json
import time
import os
from dotenv import load_dotenv


from objects.player import Player
load_dotenv()

OTHER_NODES = []
tasks = []
game = None

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
    for node in target:
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
        if "Guess" == decoded["Command"]:
            game.guess_letter(decoded["Letter"])
            await send_info({'Command':'Response OK'})

        if "Response OK" == decoded["Command"]:
            print("OK")

        if "State" == decoded["Command"]:
            print("State")
            ips = []
            sender = writer.get_extra_info('peername')
            message = decoded["State"]
            print(game)
            for player in game.get_players():
                ips.append(player.get_ip())
            for player in message["players"]:
                if player["ip"] == sender:
                    game.add_player(Player(sender))
                    ips.append(sender)
                if player["ip"] not in ips:
                    game.add_player(Player(player["ip"]))
                    await initiate_connection(player["ip"])
            for letter in message["guessed_letters"]:
                game.guess_letter(letter)

        if "Connect" == decoded["Command"]:
            OTHER_NODES.append((reader, writer))
            addr = writer.get_extra_info('peername')
            print(f"Connection from {addr}")
            game.add_player(Player(addr[0]))
            await state([(reader,writer)])
            
    

async def initiate_connection(target_host, target_port = "1999"):
    try:
        reader, writer = await asyncio.open_connection(target_host, target_port)
        print(f"Connected to {target_host}:{target_port}")
        
        await send_info({'Command': 'Connect'}, [(reader, writer)])
        OTHER_NODES.append((reader, writer))
        tasks.append(asyncio.create_task(handle_client(reader, writer)))
        

    except Exception as e:
        print(f"Failed to connect: {e}")

async def main(gameinst):
    global game
    game = gameinst
    host = os.getenv('HOST')
    port = 1999
    print(game.as_JSON())
    game.add_player(Player(host))
    await asyncio.gather(listen_for_connections(host, port), *tasks)
    

