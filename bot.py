import asyncio
import json
import websockets
import requests
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
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

async def start_bot():
    # Mensaje de inicio que se enviará sí o sí
    await send_telegram_message("✅ Bot conectado correctamente. Escuchando gemas en Pump.fun...")

    # Luego inicia el WebSocket
    uri = "wss://pumpportal.fun/api/data"
    try:
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
                        msg += f"<a href='https://pump.fun/{address}'>Mintea aquí</a>"
                        await send_telegram_message(msg)
                except Exception as e:
                    print("Error interno:", e)
    except Exception as conn_error:
        print("Error de conexión WebSocket:", conn_error)
        await send_telegram_message("⚠️ Error conectando con Pump.fun. Intentando nuevamente pronto...")

# Ejecutar
asyncio.run(start_bot())