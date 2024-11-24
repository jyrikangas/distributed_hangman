import asyncio
import json


OTHER_NODES = []

async def send_info(information):
    for node in OTHER_NODES:
        data = json.dumps({"Letter": information})
        node[1].write(data.encode())
        await node[1].drain()
        response = await node[0].read(100)
        print(response.decode())

async def listen_for_connections(host, port):
    server = await asyncio.start_server(handle_client, host, port)
    print(f"Listening for connections on {host}:{port}")
    async with server:
        await server.serve_forever()

async def handle_client(reader, writer):
    while True:
        response = await reader.read(100)
        addr = writer.get_extra_info('peername')
        print(f"Connection from {addr}")
        writer.write(b"Hello, client!\n")
        await writer.drain()
    

async def initiate_connection(target_host, target_port = "1999"):
    try:
        reader, writer = await asyncio.open_connection(target_host, target_port)
        print(f"Connected to {target_host}:{target_port}")
        writer.write(b"Hello, server!\n")
        await writer.drain()
        response = await reader.read(100)
        print(f"Received from server {target_host}: {response.decode()}")
        OTHER_NODES.append((reader,writer))
    except Exception as e:
        print(f"Failed to connect: {e}")

async def main():
    host = "192.168.68.106"
    port = 1999
    # list hosts & ports of other nodes
    other_nodes = [("host", 1999),("host", 1999)]
    
    await asyncio.gather(
        listen_for_connections(host, port),
        initiate_connection(host, port),
    )


if __name__ == "__main__":
    asyncio.run(main())
