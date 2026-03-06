import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")   # lấy token từ Railway Variables
ROLE_ID = 1479100091313946635  # thay bằng ROLE ID của bạn

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

keywords = []

@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")

# thêm keyword
@bot.command()
async def addkw(ctx, *, kw):
    keywords.append(kw)
    await ctx.send(f"✅ Đã thêm keyword: {kw}")

# xoá keyword
@bot.command()
async def delkw(ctx, *, kw):
    if kw in keywords:
        keywords.remove(kw)
        await ctx.send(f"❌ Đã xoá keyword: {kw}")
    else:
        await ctx.send("Không tìm thấy keyword")

# xem keyword
@bot.command()
async def listkw(ctx):
    if not keywords:
        await ctx.send("Chưa có keyword")
    else:
        await ctx.send("\n".join(keywords))

# monitor message
@bot.event
async def on_message(message):

    if message.author.bot:
        text = message.content.lower()

        for kw in keywords:
            if kw.lower() in text:
                role = message.guild.get_role(ROLE_ID)
                await message.channel.send(f"{role.mention} 🔔 Keyword detected: **{kw}**")
                break

    await bot.process_commands(message)

bot.run(TOKEN)
