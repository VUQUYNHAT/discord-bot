import discord
from discord.ext import commands
import os
import json

TOKEN = os.getenv("TOKEN")

ROLE_ID = 1479100091313946635      # ID role VIP
CHANNEL_ID = 1453022405222989947    # ID kênh joshin

KEYWORD_FILE = "keywords.json"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# load keyword
if os.path.exists(KEYWORD_FILE):
    with open(KEYWORD_FILE, "r") as f:
        keywords = json.load(f)
else:
    keywords = []

# lưu keyword
def save_keywords():
    with open(KEYWORD_FILE, "w") as f:
        json.dump(keywords, f)

# chống spam
last_message = ""

@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")

# thêm keyword
@bot.command()
async def addkw(ctx, *, kw):
    if kw not in keywords:
        keywords.append(kw)
        save_keywords()
        await ctx.send(f"✅ Đã thêm kw: {kw}")
    else:
        await ctx.send("Keyword đã tồn tại")

# xoá keyword
@bot.command()
async def delkw(ctx, *, kw):
    if kw in keywords:
        keywords.remove(kw)
        save_keywords()
        await ctx.send(f"❌ Đã xoá kw: {kw}")
    else:
        await ctx.send("Không tìm thấy keyword")

# xem keyword
@bot.command()
async def listkw(ctx):
    if not keywords:
        await ctx.send("Chưa có keyword")
    else:
        text = "\n".join(keywords)
        await ctx.send(f"📋 Keyword:\n{text}")

@bot.event
async def on_message(message):

    global last_message

    # ❗ chỉ đọc webhook (bỏ hết user + bot thường)
    if message.webhook_id is None:
        return

    # chạy lệnh bot (giữ nguyên)
    if message.content.startswith("!"):
        await bot.process_commands(message)
        return

    # chỉ đọc kênh joshin
    if message.channel.id != CHANNEL_ID:
        return

    text = message.content.lower()

    # đọc embed (webhook thường dùng)
    if message.embeds:
        embed = message.embeds[0]
        if embed.title:
            text += " " + embed.title.lower()
        if embed.description:
            text += " " + embed.description.lower()

    # chống spam lặp
    if text == last_message:
        return

    last_message = text

    for kw in keywords:
        if kw.lower() in text:
            role = message.guild.get_role(ROLE_ID)
            await message.channel.send(f"{role.mention} 🔔 {kw}")
            break

    await bot.process_commands(message)

bot.run(TOKEN)
