import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

print("=" * 60)
print("Discord Bot Token Verification")
print("=" * 60)

if not TOKEN:
    print("❌ ERROR: DISCORD_TOKEN not found in .env file")
    print("\nAdd this to your .env file:")
    print('DISCORD_TOKEN=your_token_here')
    exit(1)

print(f"✅ Token found: {TOKEN[:20]}...")
print(f"✅ Token length: {len(TOKEN)} characters")

# Check token format
if "." not in TOKEN or len(TOKEN.split(".")) != 3:
    print("⚠️  Token format looks invalid. It should have format: XXX.YYY.ZZZ")
else:
    print("✅ Token format appears valid")

print("\n📖 Next steps:")
print("1. Make sure this token is from a fresh regeneration")
print("2. The bot account must have at least basic permissions")
print("3. Run: python bot.py")
print("\nIf the bot still won't connect:")
print("- Check your internet connection")
print("- Verify token on Discord Developer Portal")
print("- Regenerate token if it was compromised")
print("=" * 60)
