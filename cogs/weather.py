import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from services.weather_service import get_weather
import logging
import os
logger = logging.getLogger("cogs.weather")
logger.debug("Importing cogs.weather module")
from utils.constants import MY_GUILD


# Module-level command that delegates to the Cog method. This ensures explicit
# command registration for guild-scoped syncing while preserving the Cog logic.
if MY_GUILD:
    def _guilds_decorator(func):
        return app_commands.guilds(MY_GUILD)(func)
else:
    def _guilds_decorator(func):
        return func


@_guilds_decorator
@app_commands.command(name="weather", description="Get current weather information for a location")
@app_commands.describe(location="City name or location (e.g., 'London', 'Tokyo', 'New York')")
async def weather_command(interaction: discord.Interaction, location: str) -> None:
    """Module-level command delegating to the Weather cog implementation."""
    # Delegate to the cog method to keep business logic and embed formatting unchanged
    weather_cog = Weather(interaction.client)
    await weather_cog.weather(interaction, location)



class Weather(commands.Cog):
    """Weather information commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def weather(self, interaction: discord.Interaction, location: str) -> None:
        """Display weather information for a location."""
        await interaction.response.defer()
        logger = logging.getLogger("cogs.weather")

        try:
            # Validate location
            if not location or len(location.strip()) < 1:
                await self._send_error_embed(
                    interaction,
                    "Invalid Location",
                    "Please provide a valid location name."
                )
                return

            # Fetch weather data
            weather_data = await get_weather(location.strip())

            # Handle location not found
            if weather_data is None:
                await self._send_error_embed(
                    interaction,
                    "Location Not Found",
                    f"Could not find weather data for `{location}`. Please try another location."
                )
                return

            # Create and send embed
            embed = self._create_weather_embed(weather_data, interaction.user)
            await interaction.followup.send(embed=embed)

        except Exception as e:
            logger.exception("Weather command failed")
            await self._send_error_embed(
                interaction,
                "Weather API Error",
                "Failed to fetch weather data. Please try again later."
            )

    def _create_weather_embed(
        self,
        weather_data: dict,
        requester: discord.User
    ) -> discord.Embed:
        """
        Create a formatted embed for weather data.

        Args:
            weather_data: Dictionary containing weather information from OpenWeatherMap
            requester: Discord user who requested the command

        Returns:
            Formatted discord.Embed
        """
        # Extract main weather info
        main_data = weather_data.get("main", {})
        weather_list = weather_data.get("weather", [{}])
        weather_info = weather_list[0] if weather_list else {}
        wind_data = weather_data.get("wind", {})
        clouds_data = weather_data.get("clouds", {})
        city_name = weather_data.get("name", "Unknown")
        country = weather_data.get("sys", {}).get("country", "")

        # Temperature
        temp = main_data.get("temp")
        feels_like = main_data.get("feels_like")
        temp_min = main_data.get("temp_min")
        temp_max = main_data.get("temp_max")
        humidity = main_data.get("humidity")
        pressure = main_data.get("pressure")

        # Weather description
        description = weather_info.get("main", "Unknown")
        detailed_desc = weather_info.get("description", "").title()
        icon_code = weather_info.get("icon", "01d")

        # Wind and clouds
        wind_speed = wind_data.get("speed")
        wind_deg = wind_data.get("deg")
        clouds = clouds_data.get("all")
        visibility = weather_data.get("visibility")

        # Get emoji based on weather icon
        weather_emoji = self._get_weather_emoji(icon_code)

        # Format location
        location_str = f"{city_name}, {country}" if country else city_name

        # Create embed
        embed = discord.Embed(
            title=f"{weather_emoji} {description} in {location_str}",
            description=detailed_desc,
            color=self._get_weather_color(icon_code),
            timestamp=datetime.utcnow()
        )

        # Temperature section
        # Format temperatures safely
        def fmt(v):
            try:
                return f"{v:.1f}" if isinstance(v, (int, float)) else str(v)
            except Exception:
                return str(v)

        temp_str = f"**{fmt(temp)}°C** (feels like {fmt(feels_like)}°C)"
        embed.add_field(
            name="🌡️ Temperature",
            value=temp_str,
            inline=False
        )

        # Min/Max temps
        embed.add_field(
            name="📊 Min / Max",
            value=f"`{fmt(temp_min)}°C` / `{fmt(temp_max)}°C`",
            inline=True
        )

        # Humidity
        embed.add_field(
            name="💧 Humidity",
            value=f"`{humidity}%`" if humidity is not None else "`N/A`",
            inline=True
        )

        # Pressure
        embed.add_field(
            name="🔽 Pressure",
            value=f"`{pressure} hPa`" if pressure is not None else "`N/A`",
            inline=True
        )

        # Wind section
        embed.add_field(
            name="💨 Wind",
            value=f"`{wind_speed} m/s` at `{wind_deg}°`" if wind_speed is not None else "`N/A`",
            inline=True
        )

        # Clouds
        embed.add_field(
            name="☁️ Cloudiness",
            value=f"`{clouds}%`" if clouds is not None else "`N/A`",
            inline=True
        )

        # Visibility
        visibility_km = None
        if isinstance(visibility, (int, float)):
            visibility_km = round(visibility / 1000, 1)

        embed.add_field(
            name="👁️ Visibility",
            value=f"`{visibility_km} km`" if visibility_km is not None else "`N/A`",
            inline=True
        )

        embed.set_footer(
            text=f"Requested by {requester} | OpenWeatherMap",
            icon_url=requester.display_avatar.url
        )

        return embed

    def _get_weather_emoji(self, icon_code: str) -> str:
        """Get emoji based on OpenWeatherMap icon code."""
        emoji_map = {
            "01d": "☀️",      # Clear day
            "01n": "🌙",      # Clear night
            "02d": "⛅",      # Few clouds day
            "02n": "🌙",      # Few clouds night
            "03d": "☁️",      # Scattered clouds day
            "03n": "☁️",      # Scattered clouds night
            "04d": "☁️",      # Broken clouds day
            "04n": "☁️",      # Broken clouds night
            "09d": "🌧️",     # Shower rain day
            "09n": "🌧️",     # Shower rain night
            "10d": "🌧️",     # Rain day
            "10n": "🌧️",     # Rain night
            "11d": "⛈️",      # Thunderstorm day
            "11n": "⛈️",      # Thunderstorm night
            "13d": "❄️",      # Snow day
            "13n": "❄️",      # Snow night
            "50d": "🌫️",     # Mist day
            "50n": "🌫️",     # Mist night
        }
        return emoji_map.get(icon_code, "🌤️")

    def _get_weather_color(self, icon_code: str) -> discord.Color:
        """Get embed color based on weather."""
        if "01" in icon_code:  # Clear
            return discord.Color.from_rgb(255, 200, 87)  # Golden yellow
        elif "02" in icon_code or "03" in icon_code:  # Cloudy
            return discord.Color.from_rgb(189, 189, 189)  # Gray
        elif "04" in icon_code:  # Overcast
            return discord.Color.from_rgb(120, 120, 120)  # Dark gray
        elif "09" in icon_code or "10" in icon_code:  # Rain
            return discord.Color.from_rgb(52, 152, 219)  # Blue
        elif "11" in icon_code:  # Thunderstorm
            return discord.Color.from_rgb(155, 89, 182)  # Purple
        elif "13" in icon_code:  # Snow
            return discord.Color.from_rgb(174, 194, 224)  # Light blue
        elif "50" in icon_code:  # Mist
            return discord.Color.from_rgb(127, 140, 141)  # Muted blue gray
        else:
            return discord.Color.blurple()

    async def _send_error_embed(
        self,
        interaction: discord.Interaction,
        error_title: str,
        error_message: str
    ) -> None:
        """Send a standardized error embed."""
        embed = discord.Embed(
            title=f"❌ {error_title}",
            description=error_message,
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )
        embed.set_footer(
            text=f"Requested by {interaction.user}",
            icon_url=interaction.user.display_avatar.url
        )

        if interaction.response.is_done():
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    """Load the Weather cog."""
    logger.info("Setting up Weather cog")
    # Create instance so we can reference the bound method for explicit registration
    weather_cog = Weather(bot)
    await bot.add_cog(weather_cog)
    logger.info("Weather cog added")

    # Explicitly register the module-level `weather_command` for proper scoping
    try:
        # Remove possible existing duplicate
        try:
            existing = bot.tree.get_command("weather", guild=MY_GUILD)
            if existing:
                try:
                    bot.tree.remove_command("weather", guild=MY_GUILD)
                except Exception:
                    pass
        except Exception:
            pass

        if MY_GUILD:
            bot.tree.add_command(weather_command, guild=MY_GUILD)
            logger.info(f"Weather command registered for guild {MY_GUILD.id}")
        else:
            bot.tree.add_command(weather_command)
            logger.info("Weather command registered as global command")
    except Exception:
        logger.exception("Failed to explicitly register weather command")
