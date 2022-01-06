#madd.py

import json
import discord
from discord.ext import commands


async def command(ctx:commands.Context, *jsondata): # star because every single word and shit will be seperated
    if not any([y in "support" for y in [x.name.lower() for x in ctx.author.roles]]):
        return
    data = ' '.join(jsondata)
    info:dict = json.loads(data)
    missing = [x for x in info.keys() if x not in 'title name content'.split()]
    if missing:
        await ctx.send(f"Missing one or more required parameters: {' '.join(missing)}")
        return
    name = info['name']


    macros = json.load(open('./macros.json'))
    if name in macros.keys():
        await ctx.send("That macro already exists.")
        return

    macros[name] = {}
    for x in info.keys():
        macros[name][x] = info[x]

    json.dump(macros, open('./macros.json', 'w', encoding='utf-8'))
    await ctx.send("Success adding macro.")
