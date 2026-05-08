import aiohttp
from typing import Optional, Dict, Any


async def get_github_user(username: str) -> Optional[Dict[str, Any]]:
    """
    Fetch GitHub user data using aiohttp.

    Args:
        username: GitHub username to fetch

    Returns:
        Dictionary containing parsed JSON user data, or None if user not found

    Raises:
        aiohttp.ClientError: If network request fails
        Exception: For unexpected errors
    """
    try:
        url = f"https://api.github.com/users/{username}"
        timeout = aiohttp.ClientTimeout(total=10)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as response:
                # Return None if user not found
                if response.status == 404:
                    return None

                # Handle other HTTP errors
                if response.status != 200:
                    raise Exception(f"GitHub API error: {response.status} {response.reason}")

                # Parse and return JSON
                data = await response.json()
                return data

    except aiohttp.ClientError as e:
        raise Exception(f"Network error: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to fetch GitHub user: {str(e)}")
