import asyncio
import websockets

PORT = 8765
clients = set()

async def handler(websocket):
    print("🟢 Client connected")
    clients.add(websocket)
    try:
        await websocket.wait_closed()  # просто держим соединение открытым
    except Exception as e:
        print(f"⚠️ Error in handler: {e}")
    finally:
        clients.discard(websocket)
        print("🔌 Client disconnected")

async def broadcast(text: str):
    print(f"📡 Broadcasting to {len(clients)} clients: {text}")
    disconnected = set()
    for client in clients.copy():
        try:
            await client.send(text)
        except Exception as e:
            print(f"❌ Error sending to client: {e}")
            disconnected.add(client)
    clients.difference_update(disconnected)

async def start_overlay_server():
    server = await websockets.serve(handler, "127.0.0.1", PORT)
    print(f"🌐 WebSocket server started on ws://127.0.0.1:{PORT}")
    return server

if __name__ == "__main__":
    async def main():
        await start_overlay_server()
        await asyncio.Future()  # бесконечное ожидание, чтобы сервер жил

    asyncio.run(main())
