import asyncio
import json
from objects.player import Player

OTHER_NODES = []
tasks = []
game = None

async def state():
    await send_info(game.as_JSON())

async def players():
    info = game.get_players()
    await send_info({'Players': info})

async def guess(letter):
    await send_info({'Letter': letter})

async def send_info(information):
    print(len(OTHER_NODES))
    for node in OTHER_NODES:
        data = json.dumps(information)
        node[1].write(f'{data}\n'.encode())
        await node[1].drain()
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
        print("decoded_json:", decoded_json)
        if "Letter" in decoded_json:
            decoded = json.loads(decoded_json)
            game.guess_letter(decoded["Letter"])
            writer.write(b"OK\n")
            await writer.drain()
        if "OK" in decoded_json:
            print("OK")
        if "board" in decoded_json:
            print("State")
        if "Hello" in decoded_json:
            OTHER_NODES.append((reader, writer))
            addr = writer.get_extra_info('peername')
            print(f"Connection from {addr}")
            dump = json.dumps(game.as_JSON())
            writer.write(f'{dump}\n'.encode())
            await writer.drain()
            response = await reader.readline()
            print(response.decode())
            game.add_player(Player(addr[0],len(game.get_players())+1))

    

async def initiate_connection(target_host, target_port = "1999"):
    try:
        reader, writer = await asyncio.open_connection(target_host, target_port)
        print(f"Connected to {target_host}:{target_port}")
        writer.write(b"Hello, server!\n")
        await writer.drain()
        response = await reader.readline()
        print(f"Received from server {target_host}: {response.decode()}")
        #TODO: decode game object and replace the current game object
        OTHER_NODES.append((reader, writer))
        writer.write(b'OK\n')
        tasks.append(asyncio.create_task(handle_client(reader, writer)))
        decoded_json = response.decode()
        decoded = json.loads(decoded_json)
        ips = []
        for player in game.get_players():
            ips.append(player.get_ip())
        for player in decoded["players"]:
            if player["ip"] == target_host:
                game.add_player(Player(target_host,player["id"]))
                ips.append(target_host)
            if player["ip"] not in ips:

                game.add_player(Player(player["ip"],player["id"]))
                await initiate_connection(player["ip"])
        for letter in decoded["guessed_letters"]:
            game.guess_letter(letter)
            print(player)
    except Exception as e:
        print(f"Failed to connect: {e}")

async def main(gameinst):
    global game
    game = gameinst
    host = "192.168.1.111"
    port = 1999
    print(game.as_JSON())
    game.add_player(Player(host, 1))
    await asyncio.gather(listen_for_connections(host, port), *tasks)
    

