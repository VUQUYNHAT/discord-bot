import discord
import os

TOKEN = "MTQ3OTA5NDIyMTE1MDYxNzYzMA.GpUwCU.uG4U-74K6seDrL09wz-6_G4OM0mV2uaIVdd_nM"
ROLE_ID = 1479100091313946635

KEYWORD_FILE = "keywords.txt"

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


def load_keywords():
    if not os.path.exists(KEYWORD_FILE):
        open(KEYWORD_FILE, "w").close()
    with open(KEYWORD_FILE, "r", encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]


def save_keyword(keyword):
    with open(KEYWORD_FILE, "a", encoding="utf-8") as f:
        f.write(keyword + "\n")


def remove_keyword(keyword):
    keywords = load_keywords()
    keywords = [k for k in keywords if k != keyword]

    with open(KEYWORD_FILE, "w", encoding="utf-8") as f:
        for k in keywords:
            f.write(k + "\n")


@client.event
async def on_ready():
    print(f"Bot online: {client.user}")


@client.event
async def on_message(message):

    if message.author.bot:
        return

    content = message.content.lower()

    # thêm keyword
    if content.startswith("!addkw "):
        keyword = message.content[7:].strip()

        save_keyword(keyword)

        await message.channel.send(f"✅ Keyword added: {keyword}")
        return

    # xoá keyword
    if content.startswith("!remkw "):
        keyword = message.content[7:].strip().lower()

        remove_keyword(keyword)

        await message.channel.send(f"❌ Keyword removed: {keyword}")
        return

    # list keyword
    if content == "!listkw":

        keywords = load_keywords()

        if not keywords:
            await message.channel.send("No keywords saved.")
        else:
            text = "\n".join(keywords[:50])
            await message.channel.send(f"📃 Keywords:\n{text}")

        return

    # monitor keyword
    keywords = load_keywords()

    for kw in keywords:
        if kw in content:
            role = f"<@&{ROLE_ID}>"

            await message.channel.send(
                f"{role} 🔔 Keyword detected:\n{kw}"
            )

            break


client.run(TOKEN)
