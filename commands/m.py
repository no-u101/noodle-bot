# macros

import json
import discord
from discord.ext import commands

async def command(ctx:commands.Context, *name:str):
    macro = json.load(open('./macros.json'))
    if not macro.get(name):
        await ctx.send("That macro doesn't exist.")
        return
    data = macro[' '.join(name)]
    embed = discord.Embed(title=data['title'], description=data['content'], color=discord.Colour.blurple())
    await ctx.send(embed=embed)
    await ctx.message.delete()