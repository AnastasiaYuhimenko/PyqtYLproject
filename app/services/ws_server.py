import asyncio
import json

import websockets

connected_clients = set()


async def handler(websocket):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            for client in connected_clients:
                if client != websocket:
                    await client.send(json.dumps(data))
    except websockets.ConnectionClosed:
        pass
    finally:
        connected_clients.remove(websocket)


async def start():
    async with websockets.serve(handler, "localhost", 8001):
        print("Работаем!")
        await asyncio.Future()


asyncio.run(start())
