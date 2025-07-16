# send_test.py
import asyncio
import websockets

async def send():
    uri = "ws://127.0.0.1:8765"
    async with websockets.connect(uri) as ws:
        await ws.send("💡 Hello from Python!")

asyncio.run(send())
