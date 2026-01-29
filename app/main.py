import discord
import os
from discord.ext import commands
import dotenv
from server import server_thread

dotenv.load_dotenv()

# 1. インテントの設定
intents = discord.Intents.default()
intents.message_content = True  # メッセージ内容を読み取るために必須
intents.voice_states = True     # VCへの入退室を検知するために必須

bot = commands.Bot(command_prefix="!", intents=intents)
TOKEN = os.environ.get("TOKEN")

# 2. 設定：監視したいテキストチャンネルAとBのIDを入力してください
TARGET_CHANNEL_IDS = [1454419719963541638, 1454099919744008324] 

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.event
async def on_voice_state_update(member, before, after):
    # Bot自身の入室は無視
    if member.bot:
        return

    # 「VCに参加した瞬間」を判定（以前のチャンネルがNone、新しいチャンネルがある）
    if before.channel is None and after.channel is not None:
        
        latest_message = None

        # 設定したテキストチャンネルを順に確認
        for channel_id in TARGET_CHANNEL_IDS:
            channel = bot.get_channel(channel_id)
            
            if channel:
                # 指定したチャンネルの直近100件から、入室した本人の発言を探す
                async for msg in channel.history(limit=100):
                    if msg.author.id == member.id:
                        # 複数チャンネルある場合、より新しい(created_atが大きい)方を採用
                        if latest_message is None or msg.created_at > latest_message.created_at:
                            latest_message = msg
                        break # このチャンネルで本人の最新が見つかったら、次のチャンネルの確認へ

        # 本人のメッセージが見つかった場合のみ送信
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

            # VCのインチャットへ送信
            await after.channel.send(
                content=f"**{member.display_name}** のプロフィール",
                # embed=embed,
                view=view
            )

# 3. Botの起動
server_thread()
bot.run(TOKEN)
