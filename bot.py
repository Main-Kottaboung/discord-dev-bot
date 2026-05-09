import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from utils.constants import MY_GUILD
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
DEV_GUILD = os.getenv("DEV_GUILD_ID")

# Validate TOKEN
if not TOKEN:
    logger.error("ERROR: DISCORD_TOKEN not found in .env file!")
    exit(1)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user}")
    logger.info(f"Bot ID: {bot.user.id}")
    
    try:
        if MY_GUILD:
            try:
                synced = await bot.tree.sync(guild=MY_GUILD)
                logger.info(f"Synced {len(synced)} command(s) to guild {MY_GUILD.id}")
            except Exception:
                logger.exception("Guild sync failed, falling back to global sync")
                synced = await bot.tree.sync()
                logger.info(f"Synced {len(synced)} global command(s)")
        else:
            synced = await bot.tree.sync()
            logger.info(f"Synced {len(synced)} global command(s)")
    except Exception as e:
        logger.error(f"Failed to sync commands: {e}")
    # Log all registered app commands for debugging
    try:
        commands_list = [c.name for c in bot.tree.walk_commands()]
        logger.info(f"Registered app commands: {commands_list}")
        # Log detailed info: which guilds each command is scoped to (if any)
        for c in bot.tree.walk_commands():
            try:
                guilds = getattr(c, 'guilds', None)
                guild_ids = [g.id for g in guilds] if guilds else None
            except Exception:
                guild_ids = None
            logger.info(f"Command detail: name={c.name} | guild_ids={guild_ids} | parent={getattr(c, 'parent', None)}")
        # Extra check for weather command
        try:
            weather_cmd = bot.tree.get_command("weather", guild=MY_GUILD)
            logger.info(f"bot.tree.get_command('weather', guild=MY_GUILD) -> {weather_cmd!r}")
        except Exception:
            logger.exception("Error fetching 'weather' command from tree")
    except Exception:
        logger.exception("Failed to list registered app commands")

    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game("Managing Dev Tools")
    )

@bot.event
async def on_error(event, *args, **kwargs):
    logger.error(f"Error in {event}: {args}, {kwargs}", exc_info=True)

async def load_cogs():
    cogs_to_load = ["cogs.utility", "cogs.dev", "cogs.github", "cogs.weather"]
    
    for cog in cogs_to_load:
        try:
            await bot.load_extension(cog)
            logger.info(f"Loaded cog: {cog}")
        except Exception as e:
            logger.error(f"Failed to load cog {cog}: {e}", exc_info=True)

async def main():
    async with bot:
        try:
            await load_cogs()
            logger.info("Starting bot...")
            await bot.start(TOKEN)
        except discord.LoginFailure:
            logger.error("Failed to log in. Check your DISCORD_TOKEN in .env")
        except Exception as e:
            logger.error(f"Fatal error: {e}", exc_info=True)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Startup error: {e}", exc_info=True)