import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from typing import Optional


class Utility(commands.Cog):
    """Utility commands for server and user information."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="ping",
        description="Check the bot's latency and API response time"
    )
    async def ping(self, interaction: discord.Interaction) -> None:
        """Display bot latency."""
        try:
            latency_ms = round(self.bot.latency * 1000)

            embed = discord.Embed(
                title="🏓 Pong!",
                description=f"**Bot Latency:** {latency_ms}ms",
                color=discord.Color.brand_green(),
                timestamp=datetime.utcnow()
            )
            embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.display_avatar.url)

            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await self._send_error_embed(interaction, f"Failed to fetch ping: {str(e)}")

    @app_commands.command(
        name="avatar",
        description="Display a user's avatar"
    )
    @app_commands.describe(user="The user to get the avatar of (defaults to you)")
    async def avatar(
        self,
        interaction: discord.Interaction,
        user: Optional[discord.User] = None
    ) -> None:
        """Display a user's avatar with information."""
        try:
            target_user = user or interaction.user

            embed = discord.Embed(
                title=f"{target_user.name}'s Avatar",
                color=discord.Color.blurple(),
                timestamp=datetime.utcnow()
            )
            embed.set_image(url=target_user.display_avatar.url)
            embed.add_field(
                name="Username",
                value=f"`{target_user}`",
                inline=True
            )
            embed.add_field(
                name="User ID",
                value=f"`{target_user.id}`",
                inline=True
            )
            embed.add_field(
                name="Account Created",
                value=f"<t:{int(target_user.created_at.timestamp())}:f>",
                inline=False
            )
            embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.display_avatar.url)

            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await self._send_error_embed(interaction, f"Failed to fetch avatar: {str(e)}")

    @app_commands.command(
        name="server",
        description="Display information about the current server"
    )
    async def server(self, interaction: discord.Interaction) -> None:
        """Display server information."""
        try:
            guild = interaction.guild

            if not guild:
                await self._send_error_embed(interaction, "This command can only be used in a server!")
                return

            embed = discord.Embed(
                title=f"{guild.name}",
                color=discord.Color.brand_green(),
                timestamp=datetime.utcnow()
            )

            # Server icon
            if guild.icon:
                embed.set_thumbnail(url=guild.icon.url)

            # Server info
            embed.add_field(
                name="📊 Members",
                value=f"{guild.member_count}",
                inline=True
            )
            embed.add_field(
                name="👑 Owner",
                value=f"<@{guild.owner_id}>",
                inline=True
            )
            embed.add_field(
                name="🆔 Server ID",
                value=f"`{guild.id}`",
                inline=True
            )

            # Server creation
            embed.add_field(
                name="📅 Created On",
                value=f"<t:{int(guild.created_at.timestamp())}:f>",
                inline=True
            )

            # Verification level
            embed.add_field(
                name="🔐 Verification Level",
                value=str(guild.verification_level).title(),
                inline=True
            )

            # Channel counts
            text_channels = len([c for c in guild.channels if isinstance(c, discord.TextChannel)])
            voice_channels = len([c for c in guild.channels if isinstance(c, discord.VoiceChannel)])
            embed.add_field(
                name="💬 Channels",
                value=f"Text: {text_channels} | Voice: {voice_channels}",
                inline=True
            )

            # Roles count
            embed.add_field(
                name="🏷️ Roles",
                value=f"{len(guild.roles)}",
                inline=True
            )

            # Boost info
            embed.add_field(
                name="⭐ Boosts",
                value=f"Level {guild.premium_tier} ({guild.premium_subscription_count} boosts)",
                inline=True
            )

            embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.display_avatar.url)

            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await self._send_error_embed(interaction, f"Failed to fetch server info: {str(e)}")

    @app_commands.command(
        name="userinfo",
        description="Display detailed information about a user"
    )
    @app_commands.describe(user="The user to get information about (defaults to you)")
    async def userinfo(
        self,
        interaction: discord.Interaction,
        user: Optional[discord.User] = None
    ) -> None:
        """Display detailed user information."""
        try:
            target_user = user or interaction.user
            member = None

            # Try to get member object for guild-specific info
            if interaction.guild:
                try:
                    member = await interaction.guild.fetch_member(target_user.id)
                except discord.NotFound:
                    member = None

            embed = discord.Embed(
                title=f"User Information",
                description=f"**{target_user}**",
                color=discord.Color.blurple(),
                timestamp=datetime.utcnow()
            )

            # Avatar
            embed.set_thumbnail(url=target_user.display_avatar.url)

            # User IDs and Names
            embed.add_field(
                name="👤 Username",
                value=f"`{target_user.name}`",
                inline=True
            )
            embed.add_field(
                name="🏷️ Display Name",
                value=f"`{target_user.display_name}`",
                inline=True
            )
            embed.add_field(
                name="🆔 User ID",
                value=f"`{target_user.id}`",
                inline=True
            )

            # Account info
            embed.add_field(
                name="📅 Account Created",
                value=f"<t:{int(target_user.created_at.timestamp())}:f>",
                inline=True
            )

            # Bot status
            bot_badge = "🤖 Yes" if target_user.bot else "❌ No"
            embed.add_field(
                name="Bot Account",
                value=bot_badge,
                inline=True
            )

            # System account
            system_badge = "⚙️ Yes" if target_user.system else "❌ No"
            embed.add_field(
                name="System Account",
                value=system_badge,
                inline=True
            )

            # Member-specific info (if in guild)
            if member:
                embed.add_field(
                    name="📍 Joined Server",
                    value=f"<t:{int(member.joined_at.timestamp())}:f>",
                    inline=True
                )

                # Nick
                if member.nick:
                    embed.add_field(
                        name="📝 Server Nickname",
                        value=f"`{member.nick}`",
                        inline=True
                    )

                # Status
                status_emoji = {
                    discord.Status.online: "🟢",
                    discord.Status.idle: "🟡",
                    discord.Status.dnd: "🔴",
                    discord.Status.offline: "⚫"
                }
                status = status_emoji.get(member.status, "⚫")
                embed.add_field(
                    name="Status",
                    value=f"{status} {member.status.name.title()}",
                    inline=True
                )

                # Roles
                if member.roles and len(member.roles) > 1:
                    roles_str = " ".join([role.mention for role in member.roles[1::-1]][:5])
                    if len(member.roles) > 6:
                        roles_str += f" +{len(member.roles) - 6} more"
                    embed.add_field(
                        name=f"🎖️ Roles ({len(member.roles) - 1})",
                        value=roles_str or "No roles",
                        inline=False
                    )

                # Top role
                if member.top_role and member.top_role != interaction.guild.default_role:
                    embed.add_field(
                        name="⭐ Top Role",
                        value=member.top_role.mention,
                        inline=True
                    )

            embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.display_avatar.url)

            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await self._send_error_embed(interaction, f"Failed to fetch user info: {str(e)}")

    async def _send_error_embed(
        self,
        interaction: discord.Interaction,
        error_message: str
    ) -> None:
        """Send a standardized error embed."""
        embed = discord.Embed(
            title="❌ Error",
            description=error_message,
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.display_avatar.url)

        if interaction.response.is_done():
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    """Load the Utility cog."""
    await bot.add_cog(Utility(bot))