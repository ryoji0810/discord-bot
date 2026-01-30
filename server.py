from threading import Thread

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.route('/', methods=['GET', 'HEAD']) # HEADを追加
def home():
    return "Bot is running!"

def start():
	uvicorn.run(app, host="0.0.0.0", port=8080)

def server_thread():
	t = Thread(target=start)
	t.start()
