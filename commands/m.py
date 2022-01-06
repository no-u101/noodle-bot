# macros

import json
import discord
from discord.ext import commands

async def command(ctx:commands.Context, *name:str):
    macro = json.load(open('./macros.json'))
    callname = ' '.join(name)
    if not macro.get(callname):
        await ctx.send("That macro doesn't exist.")
        return
    data = macro[callname]
    embed = discord.Embed(title=data['title'], description=data['content'], color=discord.Colour.blurple())
    await ctx.send(embed=embed)
    await ctx.message.delete()