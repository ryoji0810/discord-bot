import discord
from discord.ext import commands

class VoiceProfile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # 監視したいテキストチャンネルID
        self.target_channel_ids = [1454419719963541638, 1454099919744008324]

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return

        # 「VCに参加した瞬間」を判定
        if before.channel is None and after.channel is not None:
            latest_message = None

            # 設定したテキストチャンネルを順に確認
            for channel_id in self.target_channel_ids:
                channel = self.bot.get_channel(channel_id)
                
                if channel:
                    # 本人の発言を探す
                    async for msg in channel.history(limit=100):
                        if msg.author.id == member.id:
                            if latest_message is None or msg.created_at > latest_message.created_at:
                                latest_message = msg
                            break

            # メッセージが見つかった場合のみ送信
            if latest_message:
                # --- Embed（埋め込み）の作成 ---
                # embed = discord.Embed(
                #     title=f"#{latest_message.channel.name} でのあなたの最新発言",
                #     description=latest_message.content or "（本文なし：画像または埋め込みのみ）",
                #     color=discord.Color.blue(),
                #     timestamp=latest_message.created_at
                # )
                # embed.set_author(
                #     name=f"{member.display_name} (@{member.name})",
                #     icon_url=member.display_avatar.url
                # )
                
                # 画像が添付されていればEmbedに表示
                # if latest_message.attachments:
                #     embed.set_image(url=latest_message.attachments[0].url)

                # --- ボタン（URLリンク）の作成 ---
                view = discord.ui.View()
                btn = discord.ui.Button(
                    label="メッセージへ移動",
                    url=latest_message.jump_url,
                    style=discord.ButtonStyle.link
                )
                view.add_item(btn)

                # VCのチャットへ送信
                await after.channel.send(
                    content=f"**{member.display_name}** のプロフィール",
                    view=view
                )

async def setup(bot):
    await bot.add_cog(VoiceProfile(bot))