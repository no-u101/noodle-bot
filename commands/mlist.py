#mlist.py

import json

async def command(ctx):
    macros = json.load(open('./macros.json'))
    names = '\n'.join(list(macros.keys()))
    await ctx.send(f"All macros: {names}")