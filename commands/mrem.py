#mrem.py

import json
from discord.ext import commands

async def command(ctx:commands.Context, *name):
    callname = ' '.join(name)
    macros:dict = json.load(open('./macros.json'))
    if macros.get(callname):
        macros.pop(callname)
        json.dump(macros, open('./macros.json', 'w', encoding='utf-8'))
        await ctx.send("Success removing macro.")
    else:
        await ctx.send("That macro already doesn't exist.")