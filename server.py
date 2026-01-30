from threading import Thread

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/') # route ではなく get
async def home(request=None):
    return "Bot is running!"

def start():
	uvicorn.run(app, host="0.0.0.0", port=8080)

def server_thread():
	t = Thread(target=start)
	t.start()
