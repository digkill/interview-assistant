import asyncio
import threading
import tkinter as tk
import websockets

WS_URL = "ws://127.0.0.1:8765"

class TransparentOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GPT Overlay")
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)
        self.root.geometry("600x100+100+100")
        self.root.configure(bg="black")
        self.root.wm_attributes("-alpha", 0.85)

        self.text_var = tk.StringVar()
        self.text_var.set("🤖 Waiting for message...")

        self.label = tk.Label(
            self.root,
            textvariable=self.text_var,
            font=("Arial", 20),
            fg="white",
            bg="black",
            justify="left",
            wraplength=580,
        )
        self.label.pack(padx=10, pady=10)

    def update_text(self, text):
        # Обновление текста безопасно через after
        self.root.after(0, self.text_var.set, text)

    def run(self):
        self.root.mainloop()

overlay = TransparentOverlay()

async def listen_to_server():
    while True:
        try:
            print("🔄 Connecting to WebSocket server...")
            async with websockets.connect(WS_URL) as websocket:
                print("🟢 Connected to server")
                overlay.update_text("🟢 Connected to server. Waiting for messages...")

                while True:
                    message = await websocket.recv()
                    print(f"📥 {message}")
                    overlay.update_text(message)

        except Exception as e:
            print(f"❌ Connection error: {e}")
            overlay.update_text("❌ Connection error. Retrying in 3s...")
            await asyncio.sleep(3)

def start_async_loop():
    asyncio.run(listen_to_server())

# Запускаем asyncio в фоновом потоке
threading.Thread(target=start_async_loop, daemon=True).start()

# Запускаем tkinter GUI в главном потоке
overlay.run()
