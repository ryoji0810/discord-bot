import discord
from discord.ext import commands
import os
import dotenv
from server import server_thread

dotenv.load_dotenv()
TOKEN = os.environ.get("TOKEN")

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and not filename.startswith("__"):
                await self.load_extension(f"cogs.{filename.removesuffix('.py')}")
                print(f"Loaded extension: {filename}")

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

if __name__ == "__main__":
    server_thread()
    bot = MyBot()
    bot.run(TOKEN)
