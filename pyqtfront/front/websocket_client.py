import asyncio
import json
import threading

import websockets


class WebSocketClient:
    def __init__(self, user_id: int, message_callback):
        self.user_id = user_id
        self.message_callback = message_callback
        self.loop = asyncio.new_event_loop()
        self.ws = None
        self.thread = threading.Thread(target=self.run_loop, daemon=True)
        self.thread.start()

    def run_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.connect())

    async def connect(self):
        uri = f"ws://localhost:8001/ws/{self.user_id}"
        async with websockets.connect(uri) as ws:
            self.ws = ws
            while True:
                data = await ws.recv()
                msg = json.loads(data)
                self.message_callback(msg)

    def send_message(self, msg_data: dict):
        if self.ws:
            asyncio.run_coroutine_threadsafe(
                self.ws.send(json.dumps(msg_data)), self.loop
            )
