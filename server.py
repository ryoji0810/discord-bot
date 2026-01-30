from threading import Thread

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.api_route("/", methods=["GET", "HEAD"])
async def home(request: Request):
    return {"message": "Bot is running!"}

def start():
	uvicorn.run(app, host="0.0.0.0", port=8080)

def server_thread():
	t = Thread(target=start)
	t.start()
