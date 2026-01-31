import discord
from discord.ext import commands
import os

class VoiceProfile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        env_channels = os.getenv("TARGET_CHANNEL_IDS", "")

        if env_channels:
            self.target_channel_ids = [int(id_str.strip()) for id_str in env_channels.split(",")]
        else:
            self.target_channel_ids = []
            
        self.sent_messages = {}

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return

        # --- VCに入室したとき ---
        if before.channel is None and after.channel is not None:
            latest_message = None

            for channel_id in self.target_channel_ids:
                channel = self.bot.get_channel(channel_id)
                if channel:
                    async for msg in channel.history(limit=100):
                        if msg.author.id == member.id:
                            if latest_message is None or msg.created_at > latest_message.created_at:
                                latest_message = msg
                            break

            if latest_message:
                view = discord.ui.View()
                btn = discord.ui.Button(
                    label="プロフィールへ移動",
                    url=latest_message.jump_url,
                    style=discord.ButtonStyle.link
                )
                view.add_item(btn)

                # 送信したメッセージを記録しておく
                bot_msg = await after.channel.send(
                    content=f"**{member.display_name}** のプロフィール",
                    view=view
                )
                self.sent_messages[member.id] = bot_msg

        # --- VCを完全に退出したとき ---
        elif before.channel is not None and after.channel is None:
            # 記録されているメッセージがあれば削除
            bot_msg = self.sent_messages.pop(member.id, None)
            if bot_msg:
                try:
                    await bot_msg.delete()
                except discord.NotFound:
                    pass  # すでに手動で削除されていた場合など
                except discord.Forbidden:
                    print("メッセージの削除権限がありません。")

async def setup(bot):
    await bot.add_cog(VoiceProfile(bot))
