import random
import asyncio
import requests # check to see if the map exists

async def command(ctx):
    mess = await ctx.send("Finding random existing map...")
    rand = hex(random.randint(1,0xfffff))[2:]
    r = requests.get(f'https://beatsaver.com/api/maps/id/{rand}')
    while r.status_code == 404:
        rand = hex(random.randint(1,0xfffff))[2:]
        r = requests.get(f'https://beatsaver.com/api/maps/id/{rand}')
        if r.status_code != 404:
            break
        await asyncio.sleep(3)
    
    await mess.edit(content=f"Your random ID is {rand}. https://beatsaver.com/maps/{rand}")
