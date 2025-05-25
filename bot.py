
import asyncio
import json
import websockets
import requests
import os

TELEGRAM_TOKEN = "8124603541:AAHZzrF_-0T85KjjkMwHq0O-PhWIxT2A6fI"
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # se configurará en Render

async def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("Error sending message:", e)

async def listen_pumpfun():
    url = "wss://pump.fun/ws"

    async with websockets.connect(url) as ws:
        await ws.send(json.dumps({"type": "subscribe", "channel": "tokens"}))

        while True:
            try:
                message = await ws.recv()
                data = json.loads(message)

                if "token" in data:
                    token = data["token"]
                    name = token.get("name")
                    address = token.get("address")
                    volume = token.get("volume", 0)

                    if volume > 0.1:
                        msg = f"<b>Nuevo token detectado:</b> {name}\n"
                        msg += f"Volumen inicial: {volume:.2f} SOL\n"
                        msg += f"<a href='https://pump.fun/{address}'>Ir al token</a>"
                        await send_telegram_message(msg)

            except Exception as e:
                print("Error:", e)

if __name__ == "__main__":
    asyncio.run(listen_pumpfun())
