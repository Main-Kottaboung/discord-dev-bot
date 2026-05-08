import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    await bot.tree.sync()

    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game("Managing Dev Tools")
    )

    print(f"Logged in as {bot.user}")

async def load_cogs():
    await bot.load_extension("cogs.utility")
    await bot.load_extension("cogs.dev")
    await bot.load_extension("cogs.github")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

asyncio.run(main())