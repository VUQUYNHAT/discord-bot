import discord
import os

TOKEN = "MTQ3OTA5NDIyMTE1MDYxNzYzMA.GQmOcA.Ep2GvsI2Rx_Z7f9HYvYeXh5GcRTLhc09dkNYBY"

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

ROLE_ID = 123456789012345678  # id role
KEYWORDS = ["pokemon", "restock", "stock"]

@client.event
async def on_ready():
    print(f"Bot logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()

    for word in KEYWORDS:
        if word in content:
            role = message.guild.get_role(ROLE_ID)
            await message.channel.send(f"{role.mention} Keyword detected: {word}")
            break

client.run(TOKEN)
