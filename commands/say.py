#say.py

import asyncio

async def command(ctx, *args):
    
    if any([y in "administrator staff founder" for y in [x.name.lower() for x in ctx.author.roles]]):
        c = ctx.guild.get_channel(int(args[0]))
        message = ' '.join(args[1:])
        time = len(message) / 10
        for _ in range(int(time/10)):
            await c.trigger_typing()
            await asyncio.sleep(10)
        await c.send(message)
    
