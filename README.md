# Discord Dev Bot

A production-grade Discord bot built with discord.py 2.x featuring utility commands, GitHub integration, and developer tools.

## Features

### 🛠️ Utility Commands (`/utility`)
- **`/ping`** — Check bot latency and API response time
- **`/avatar [user]`** — Display a user's avatar with account information
- **`/server`** — View detailed server information (members, channels, roles, boosts)
- **`/userinfo [user]`** — Get comprehensive user information (account age, roles, status, etc.)

### 🐙 GitHub Integration (`/github`)
- **`/github <username>`** — Fetch GitHub user profiles with:
  - Avatar and profile link
  - Bio and account creation date
  - Followers, following, and public repos count
  - Location, company, and website information
  - Graceful error handling for invalid usernames

### 🌤️ Weather Information (`/weather`)
- **`/weather <location>`** — Get current weather data with:
  - Real-time temperature, feels-like, min/max
  - Humidity, pressure, and wind information
  - Cloud coverage and visibility
  - Dynamic emoji and color-coded embeds
  - Support for any city worldwide

## Requirements

- Python 3.9+
- discord.py 2.0+
- aiohttp (for API calls)
- python-dotenv (for environment variables)

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd discord-dev-bot
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
Create a `.env` file in the root directory:
```env
DISCORD_TOKEN=your_bot_token_here
WEATHER_API_KEY=your_openweathermap_api_key_here
```

Get a free OpenWeatherMap API key: https://openweathermap.org/api

### 5. Run the Bot
```bash
python bot.py
```

## Project Structure

```
discord-dev-bot/
├── bot.py                 # Main bot entry point
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in repo)
├── .gitignore             # Git ignore file
│
├── cogs/                  # Command cogs
│   ├── utility.py        # Utility commands (ping, avatar, server, userinfo)
│   ├── github.py         # GitHub integration command
│   ├── weather.py        # Weather information command
│   └── dev.py            # Developer commands
│
├── services/              # Business logic layer
│   ├── github_service.py # GitHub API interaction service
│   └── weather_service.py # OpenWeatherMap API service
│
└── utils/                 # Utility functions
    └── embeds.py         # Common embed utilities
```

## Usage Examples

### Utility Commands
```
/ping                              # Check bot latency
/avatar @username                  # View someone's avatar
/avatar                            # View your own avatar
/server                            # View server information
/userinfo @username                # Get user information
/userinfo                          # View your own information
```

### GitHub Commands
```
/github torvalds                   # Get Linus Torvalds' profile
/github gvanrossum                 # Get Guido van Rossum's profile
```

### Weather Commands
```
/weather London                    # Get weather for London
/weather Tokyo                     # Get weather for Tokyo
/weather "New York"                # Get weather for New York
```

## Architecture

This bot follows **clean architecture** principles:

```
Discord Commands (Cogs)
        ↓
    Discord Bot
        ↓
    Services Layer
        ↓
    External APIs (GitHub)
```

### Service Layer Benefits
- API logic isolated and reusable
- Easy to test and maintain
- Dependency injection ready
- Clear separation of concerns

## Error Handling

The bot gracefully handles:
- Invalid usernames (GitHub)
- Network timeouts
- User not found errors
- API rate limiting
- Missing permissions

All errors return user-friendly embeds.

## Command Response Format

All commands use **modern Discord embeds** with:
- Clean, professional styling
- Emoji indicators for visual clarity
- Timestamps for context
- Requester footer with avatar
- Consistent color scheme

## Configuration

### Bot Intents
The bot requires these intents:
- `message_content` — For message processing
- `members` — For member information
- `default` — Standard bot permissions

### Slash Commands
All commands use Discord's native slash commands (app_commands).

## API Integrations

### GitHub API
- **Endpoint**: `https://api.github.com`
- **Rate Limit**: 60 requests per hour (unauthenticated)
- **Timeout**: 10 seconds
- **Session**: Persistent aiohttp session for efficiency

### OpenWeatherMap API
- **Endpoint**: `https://api.openweathermap.org/data/2.5/weather`
- **Units**: Metric (Celsius, m/s)
- **Timeout**: 10 seconds
- **Free Tier**: 1,000 calls/day
- **Sign Up**: https://openweathermap.org/api

## Development

### Adding New Commands
1. Create a new method in a cog with `@app_commands.command()` decorator
2. Use `discord.Embed` for responses
3. Include error handling with try/except
4. Add type hints

### Adding New Services
1. Create service file in `services/` directory
2. Use aiohttp for async operations
3. Define custom exceptions
4. Implement error handling

## Troubleshooting

### Bot doesn't start
- Check `DISCORD_TOKEN` in `.env` file
- Verify Python version is 3.9+
- Install all dependencies: `pip install -r requirements.txt`

### Commands not appearing
- Restart the bot (commands sync on startup via `await bot.tree.sync()`)
- Ensure bot has `applications.commands` scope

### Slow GitHub API responses
- GitHub API may be rate limited
- Consider implementing caching for frequently requested users

## Dependencies

```
discord.py>=2.0.0
aiohttp>=3.8.0
python-dotenv>=0.19.0
```

See [requirements.txt](requirements.txt) for exact versions.

## License

This project is provided as-is for educational and personal use.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review Discord.py documentation: https://discordpy.readthedocs.io/
3. Visit GitHub API docs: https://docs.github.com/en/rest

---

**Built with ❤️ using discord.py 2.x**
