import asyncio
import tkinter as tk
import websockets
import threading

PORT = 8765
clients = set()

# 👁️ GUI overlay
class TransparentOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Overlay Server")
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)
        self.root.geometry("600x600+600+600")
        self.root.configure(bg='black')
        self.root.wm_attributes("-alpha", 0.85)

        self.text_var = tk.StringVar()
        self.text_var.set("🟢 Server is running...")

        self.label = tk.Label(self.root, textvariable=self.text_var,
                              font=("Arial", 20), fg="white", bg="black", justify="left", wraplength=580)
        self.label.pack(padx=10, pady=10)

    def update_text(self, text):
        self.text_var.set(text)

    def run(self):
        self.root.mainloop()

overlay = TransparentOverlay()

# 🌐 WebSocket обработка
async def handler(websocket):
    print("🟢 Client connected")
    clients.add(websocket)
    try:
        async for message in websocket:
            print(f"📥 {message}")
            overlay.root.after(0, overlay.update_text, message)
            await broadcast(message)
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

async def start_server():
    server = await websockets.serve(handler, "127.0.0.1", PORT)
    print(f"🌐 WebSocket server started on ws://127.0.0.1:{PORT}")
    return server

def run_async_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_server())
    loop.run_forever()

# 🚀 Запуск WebSocket сервера в отдельном потоке
threading.Thread(target=run_async_loop, daemon=True).start()

# 🖼️ Запуск GUI
overlay.run()
