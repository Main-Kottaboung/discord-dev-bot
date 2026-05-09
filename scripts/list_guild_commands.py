import os
import sys
import json
from dotenv import load_dotenv
import aiohttp
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DEV_GUILD_ID')
if not TOKEN or not GUILD:
    print('DISCORD_TOKEN or DEV_GUILD_ID missing in .env')
    sys.exit(1)

API = 'https://discord.com/api/v10'

async def main():
    headers = {'Authorization': f'Bot {TOKEN}'}
    async with aiohttp.ClientSession() as sess:
        # get application id
        async with sess.get(f'{API}/oauth2/applications/@me', headers=headers) as r:
            app = await r.json()
            print('app:', json.dumps(app, indent=2))
            app_id = app.get('id')
            if not app_id:
                print('Could not get application id')
                return
        async with sess.get(f'{API}/applications/{app_id}/commands', headers=headers) as r:
            global_cmds = await r.json()
            print('global commands:', json.dumps(global_cmds, indent=2))

        async with sess.get(f'{API}/applications/{app_id}/guilds/{GUILD}/commands', headers=headers) as r:
            guild_cmds = await r.json()
            print('guild commands:', json.dumps(guild_cmds, indent=2))

asyncio.run(main())
