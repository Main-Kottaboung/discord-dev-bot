import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from services.github_service import github_service, GitHubUserNotFound, GitHubServiceError


class GitHub(commands.Cog):
    """GitHub user information commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="github",
        description="Fetch information about a GitHub user"
    )
    @app_commands.describe(username="The GitHub username to look up")
    async def github_user(self, interaction: discord.Interaction, username: str) -> None:
        """Display GitHub user information."""
        # Defer the response as GitHub API might take a moment
        await interaction.response.defer()

        try:
            # Validate username format
            if not username or len(username) < 1:
                await self._send_error_embed(
                    interaction,
                    "Invalid username",
                    "Please provide a valid GitHub username."
                )
                return

            # Fetch user data from GitHub API
            user_data = await github_service.get_user(username.strip())

            # Create and send embed
            embed = await self._create_user_embed(user_data, interaction.user)
            await interaction.followup.send(embed=embed)

        except GitHubUserNotFound:
            await self._send_error_embed(
                interaction,
                "User Not Found",
                f"Could not find GitHub user `{username}`. Please check the username and try again."
            )
        except GitHubServiceError as e:
            await self._send_error_embed(
                interaction,
                "GitHub API Error",
                f"Failed to fetch user data: {str(e)}"
            )
        except Exception as e:
            await self._send_error_embed(
                interaction,
                "Unexpected Error",
                f"An unexpected error occurred: {str(e)}"
            )

    async def _create_user_embed(
        self,
        user_data: dict,
        requester: discord.User
    ) -> discord.Embed:
        """
        Create a formatted embed for GitHub user data.

        Args:
            user_data: Dictionary containing user information
            requester: Discord user who requested the command

        Returns:
            Formatted discord.Embed
        """
        # Parse creation date
        try:
            created_at_str = user_data["created_at"]
            created_at = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
            created_at_display = f"<t:{int(created_at.timestamp())}:f>"
        except (ValueError, KeyError):
            created_at_display = "Unknown"

        # Create embed
        embed = discord.Embed(
            title=f"{user_data['name']}",
            description=user_data["bio"],
            url=user_data["profile_url"],
            color=discord.Color.from_rgb(88, 88, 88),  # GitHub dark gray
            timestamp=datetime.utcnow()
        )

        # Avatar
        if user_data["avatar_url"]:
            embed.set_thumbnail(url=user_data["avatar_url"])

        # Username and ID
        embed.add_field(
            name="👤 GitHub Username",
            value=f"[`{user_data['username']}`]({user_data['profile_url']})",
            inline=True
        )

        # Stats row 1
        embed.add_field(
            name="👥 Followers",
            value=f"`{user_data['followers']:,}`",
            inline=True
        )
        embed.add_field(
            name="🔗 Following",
            value=f"`{user_data['following']:,}`",
            inline=True
        )

        # Stats row 2
        embed.add_field(
            name="📦 Public Repos",
            value=f"`{user_data['public_repos']:,}`",
            inline=True
        )

        embed.add_field(
            name="📅 Account Created",
            value=created_at_display,
            inline=True
        )

        # Spacer
        embed.add_field(
            name="",
            value="",
            inline=True
        )

        # Additional info
        if user_data["company"] != "Not specified":
            embed.add_field(
                name="🏢 Company",
                value=user_data["company"],
                inline=True
            )

        if user_data["location"] != "Not specified":
            embed.add_field(
                name="📍 Location",
                value=user_data["location"],
                inline=True
            )

        if user_data["blog"] != "None":
            embed.add_field(
                name="🌐 Website",
                value=f"[Visit]({user_data['blog']})",
                inline=True
            )

        embed.set_footer(
            text=f"Requested by {requester}",
            icon_url=requester.display_avatar.url
        )

        return embed

    async def _send_error_embed(
        self,
        interaction: discord.Interaction,
        error_title: str,
        error_message: str
    ) -> None:
        """
        Send a standardized error embed.

        Args:
            interaction: Discord interaction object
            error_title: Title of the error
            error_message: Error description
        """
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
    """Load the GitHub cog."""
    await bot.add_cog(GitHub(bot))
