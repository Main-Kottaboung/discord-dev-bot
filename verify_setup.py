"""
Discord Bot Setup Verification Checklist
Run this to verify your bot is properly configured
"""

import os
from dotenv import load_dotenv
import sys

print("\n" + "="*70)
print("DISCORD BOT SETUP VERIFICATION CHECKLIST")
print("="*70)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
WEATHER_KEY = os.getenv("WEATHER_API_KEY")

# Check 1: Environment Variables
print("\n1️⃣  ENVIRONMENT VARIABLES")
print("-" * 70)

if TOKEN:
    print(f"   ✅ DISCORD_TOKEN found: {TOKEN[:30]}...")
    # Check token format
    parts = TOKEN.split(".")
    if len(parts) == 3:
        print(f"   ✅ Token format valid (3 parts)")
    else:
        print(f"   ❌ Token format invalid (should have 3 parts, has {len(parts)})")
else:
    print("   ❌ DISCORD_TOKEN NOT found in .env")

if WEATHER_KEY:
    print(f"   ✅ WEATHER_API_KEY found")
else:
    print("   ⚠️  WEATHER_API_KEY not found (optional, weather command will fail)")

# Check 2: Dependencies
print("\n2️⃣  PYTHON DEPENDENCIES")
print("-" * 70)

dependencies = {
    "discord": "discord.py",
    "aiohttp": "aiohttp",
    "dotenv": "python-dotenv",
}

all_deps_ok = True
for module, package_name in dependencies.items():
    try:
        __import__(module)
        print(f"   ✅ {package_name} installed")
    except ImportError:
        print(f"   ❌ {package_name} NOT installed")
        all_deps_ok = False

if not all_deps_ok:
    print("\n   Install missing packages:")
    print("   pip install -r requirements.txt")

# Check 3: File Structure
print("\n3️⃣  PROJECT FILE STRUCTURE")
print("-" * 70)

required_files = {
    "bot.py": "Main bot file",
    "cogs/utility.py": "Utility commands",
    "cogs/github.py": "GitHub integration",
    "cogs/weather.py": "Weather commands",
    "services/github_service.py": "GitHub API service",
    "services/weather_service.py": "Weather API service",
}

for file_path, description in required_files.items():
    if os.path.exists(file_path):
        print(f"   ✅ {file_path:<35} ({description})")
    else:
        print(f"   ❌ {file_path:<35} MISSING")

# Check 4: Discord Bot Setup
print("\n4️⃣  DISCORD BOT SETUP (Manual Verification Required)")
print("-" * 70)
print("""
   Go to: https://discord.com/developers/applications
   
   ✅ Verify:
      □ Bot is created and named
      □ TOKEN is valid (regenerate if unsure)
      □ OAuth2 > Scopes has: applications.commands
      □ OAuth2 > Permissions has:
        - Send Messages
        - Embed Links
        - Attach Files
      □ Bot is invited to your test server
        (Use OAuth2 > URL Generator with scopes + permissions)
      □ Bot has required intents enabled:
        - MESSAGE CONTENT INTENT
        - SERVER MEMBERS INTENT
""")

# Check 5: Recommendations
print("\n5️⃣  TROUBLESHOOTING STEPS")
print("-" * 70)
print("""
   If bot still won't connect:
   
   1. Regenerate Token:
      - Discord Developer Portal
      - Applications > Your Bot
      - Token > Reset Token
      - Copy new token to .env
   
   2. Verify Bot Permissions:
      - Make sure bot can send messages in channels
      - Check server permissions aren't blocking it
   
   3. Test Connection:
      - Run: python bot.py
      - Look for "Logged in as [BotName]" message
      - If it hangs, token is likely invalid
   
   4. Check Internet:
      - Try: ping discord.gg
      - Ensure firewall isn't blocking Python
   
   5. Check .env File:
      - Should be in project root: d:\\work\\main_code_playground\\discord-dev-bot\\.env
      - Should have DISCORD_TOKEN (no spaces around =)
""")

print("\n" + "="*70)
print("NEXT STEP: Run 'python bot.py' and check for:")
print("  ✅ 'Logged in as [YourBotName]'")
print("  ✅ 'Synced X command(s)'")
print("="*70 + "\n")
