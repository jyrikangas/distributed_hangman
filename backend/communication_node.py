import asyncio

async def listen_for_connections(host, port):
    server = await asyncio.start_server(handle_client, host, port)
    print(f"Listening for connections on {host}:{port}")
    async with server:
        await server.serve_forever()

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Connection from {addr}")
    writer.write(b"Hello, client!\n")
    await writer.drain()
    writer.close()

async def initiate_connection(target_host, target_port):
    try:
        reader, writer = await asyncio.open_connection(target_host, target_port)
        print(f"Connected to {target_host}:{target_port}")
        writer.write(b"Hello, server!\n")
        await writer.drain()
        response = await reader.read(100)
        print(f"Received from server {target_host}: {response.decode()}")
        writer.close()
    except Exception as e:
        print(f"Failed to connect: {e}")

async def main():
    host = "0.0.0.0"
    port = 1999
    # list hosts & ports of other nodes
    other_nodes = [("host", 1999),("host", 1999)]
    # for host, port in other_nodes:
    
    await asyncio.gather(
        listen_for_connections(host, port),
        initiate_connection(host, port),
    )

asyncio.run(main())
