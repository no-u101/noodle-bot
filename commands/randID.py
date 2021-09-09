import random
import asyncio
import requests # check to see if the map exists

async def command(ctx):
    attempts = 0
    mess = await ctx.send(f"Finding random existing map... Attempt {attempts+1}")
    rand = hex(random.randint(1,0xfffff))[2:]
    r = requests.get(f'https://beatsaver.com/api/maps/id/{rand}')
    if r.status_code == 404:
        while True:
            rand = hex(random.randint(1,0xfffff))[2:]
            r = requests.get(f'https://beatsaver.com/api/maps/id/{rand}')
            if r.status_code != 404:
                break
            attempts += 1
            await mess.edit(content=f"Finding random existing map... Attempt {attempts+1}")
            await asyncio.sleep(1)
    
    await mess.edit(content=f"Your random ID is {rand}. https://beatsaver.com/maps/{rand}")
