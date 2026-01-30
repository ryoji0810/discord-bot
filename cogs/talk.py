import discord
from discord import app_commands
from discord.ext import commands
import random
import json
import os

class TalkCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.json_path = "topics.json" # JSONファイルのパス

    def load_topics(self):
        """JSONファイルから話題を読み込むヘルパー関数"""
        if not os.path.exists(self.json_path):
            return ["話題リストが見つかりません。"]
        
        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("talk_topics", ["話題が登録されていません。"])

    @app_commands.command(name="topic", description="JSONから話題をランダムに出します")
    async def topic(self, interaction: discord.Interaction):
        # コマンド実行のたびに読み込むと、ファイルを書き換えただけで反映されます
        topics = self.load_topics()
        selected = random.choice(topics)
        await interaction.response.send_message(f"💬 **トークテーマ:** {selected}")

async def setup(bot):
    await bot.add_cog(TalkCog(bot))