
import asyncio
import json
import websockets
import requests
import os

TELEGRAM_TOKEN = "8124603541:AAHZzrF_-0T85KjjkMwHq0O-PhWIxT2A6fI"
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

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

async def listen_new_tokens():
    uri = "wss://pumpportal.fun/api/data"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({ "method": "subscribeNewToken" }))
        while True:
            try:
                response = await websocket.recv()
                data = json.loads(response)
                if data.get("type") == "new_token":
                    token = data.get("data", {})
                    name = token.get("name", "Sin nombre")
                    address = token.get("address", "N/A")
                    msg = f"<b>NUEVO TOKEN DETECTADO:</b> {name}\n"
                    msg += f"<a href='https://pump.fun/{address}'>Ir al token</a>"
                    await send_telegram_message(msg)
            except Exception as e:
                print("Error:", e)

if __name__ == "__main__":
    asyncio.run(listen_new_tokens())
