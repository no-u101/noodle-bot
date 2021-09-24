#say.py
async def command(ctx, *args):
    
    if any([y in "administrator staff founder" for y in [x.name.lower() for x in ctx.author.roles]]):
        c = ctx.guild.get_channel(int(args[0]))
        await c.send(' '.join(args[1:]))
    
