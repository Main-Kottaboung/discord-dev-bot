import os
import sys
import json
from dotenv import load_dotenv
import aiohttp
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    print('DISCORD_TOKEN missing in .env')
    sys.exit(1)

API = 'https://discord.com/api/v10'

async def main():
    headers = {'Authorization': f'Bot {TOKEN}'}
    async with aiohttp.ClientSession() as sess:
        # get application id
        async with sess.get(f'{API}/oauth2/applications/@me', headers=headers) as r:
            app = await r.json()
            app_id = app.get('id')
            if not app_id:
                print('Could not get application id')
                return
        # list global commands
        async with sess.get(f'{API}/applications/{app_id}/commands', headers=headers) as r:
            global_cmds = await r.json()
            weather_cmd = None
            for c in global_cmds:
                if c.get('name') == 'weather':
                    weather_cmd = c
                    break
            if not weather_cmd:
                print('No global weather command found')
                return
            print('Found global weather command:', json.dumps(weather_cmd, indent=2))
        # delete it
        cmd_id = weather_cmd['id']
        async with sess.delete(f'{API}/applications/{app_id}/commands/{cmd_id}', headers=headers) as r:
            if r.status == 204:
                print('Deleted global weather command', cmd_id)
            else:
                print('Failed to delete global weather command', await r.text())

asyncio.run(main())
