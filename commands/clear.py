import asyncio

async def command(ctx, *args):
    messages = await ctx.channel.history(limit=int(args[0])+1).flatten()
    for x in messages:
        await x.delete()
    
    m = await ctx.send("Finished Clearing Messages")

    await asyncio.sleep(5)
    await m.delete()