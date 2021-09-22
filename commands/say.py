#say.py
async def command(ctx, *args):
    if any(["administrator staff founder".__contains__(y) for y in [x.name.lower() for x in ctx.author.roles]]):
        c = ctx.guild.get_channel(int(args[0]))
        await c.send(' '.join(args[1:]))
