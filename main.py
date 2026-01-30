import discord
from discord.ext import commands
import os
import dotenv
from server import server_thread

dotenv.load_dotenv()
TOKEN = os.environ.get("TOKEN")
GUILD = os.environ.get("GUILD")
MY_GUILD = discord.Object(id=GUILD)

class DiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # cogの読み込み
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and not filename.startswith("__"):
                await self.load_extension(f"cogs.{filename.removesuffix('.py')}")
                print(f"Loaded extension: {filename}")

        # そのサーバー専用に同期
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)
        print("Slash commands synced!")

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

if __name__ == "__main__":
    server_thread()
    bot = DiscordBot()
    bot.run(TOKEN)
