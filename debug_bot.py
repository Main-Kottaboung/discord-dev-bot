"""
Debug script to test bot connection and commands
"""

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    print("❌ No token found!")
    exit(1)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"\n{'='*60}")
    print(f"✅ BOT CONNECTED!")
    print(f"{'='*60}")
    print(f"Bot Name: {bot.user}")
    print(f"Bot ID: {bot.user.id}")
    print(f"{'='*60}\n")
    
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash command(s):")
        for cmd in synced:
            print(f"   - /{cmd.name}")
        print()
    except Exception as e:
        print(f"❌ Error syncing commands: {e}\n")

@bot.event
async def on_error(event, *args, **kwargs):
    print(f"❌ ERROR in {event}:")
    import traceback
    traceback.print_exc()

@bot.tree.command(name="test", description="Test if bot is responding")
async def test_command(interaction: discord.Interaction):
    """Simple test command"""
    await interaction.response.send_message("✅ Bot is responding!")

async def main():
    async with bot:
        try:
            print("🔄 Connecting to Discord...")
            await bot.start(TOKEN)
        except discord.LoginFailure:
            print("❌ LOGIN FAILED - Invalid token!")
        except Exception as e:
            print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(main())
