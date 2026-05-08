import aiohttp
from typing import Optional, Dict, Any
from datetime import datetime


class GitHubServiceError(Exception):
    """Base exception for GitHub service errors."""
    pass


class GitHubUserNotFound(GitHubServiceError):
    """Raised when GitHub user is not found."""
    pass


class GitHubService:
    """Service for interacting with GitHub API."""

    BASE_URL = "https://api.github.com"
    TIMEOUT = aiohttp.ClientTimeout(total=10)

    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(timeout=self.TIMEOUT)
        return self.session

    async def close(self) -> None:
        """Close the aiohttp session."""
        if self.session and not self.session.closed:
            await self.session.close()

    async def get_user(self, username: str) -> Dict[str, Any]:
        """
        Fetch GitHub user data.

        Args:
            username: GitHub username to fetch

        Returns:
            Dictionary containing user data

        Raises:
            GitHubUserNotFound: If user does not exist
            GitHubServiceError: For other API errors
        """
        try:
            session = await self._get_session()
            url = f"{self.BASE_URL}/users/{username}"

            async with session.get(url) as response:
                if response.status == 404:
                    raise GitHubUserNotFound(f"GitHub user '{username}' not found")

                if response.status != 200:
                    raise GitHubServiceError(
                        f"GitHub API error: {response.status} {response.reason}"
                    )

                data = await response.json()
                return self._parse_user_data(data)

        except aiohttp.ClientError as e:
            raise GitHubServiceError(f"Network error: {str(e)}")

    def _parse_user_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse and clean GitHub API response.

        Args:
            raw_data: Raw response from GitHub API

        Returns:
            Cleaned user data dictionary
        """
        return {
            "username": raw_data.get("login", "Unknown"),
            "name": raw_data.get("name") or raw_data.get("login", "Unknown"),
            "avatar_url": raw_data.get("avatar_url", ""),
            "bio": raw_data.get("bio") or "No bio provided",
            "followers": raw_data.get("followers", 0),
            "following": raw_data.get("following", 0),
            "public_repos": raw_data.get("public_repos", 0),
            "created_at": raw_data.get("created_at", ""),
            "updated_at": raw_data.get("updated_at", ""),
            "profile_url": raw_data.get("html_url", ""),
            "location": raw_data.get("location") or "Not specified",
            "blog": raw_data.get("blog") or "None",
            "company": raw_data.get("company") or "Not specified",
        }


# Global service instance
github_service = GitHubService()
