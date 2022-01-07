#madd.py

import json
import discord
from discord.ext import commands


async def command(ctx:commands.Context, *jsondata): # star because every single word and shit will be seperated
    if not any([y in "support" for y in [x.name.lower() for x in ctx.author.roles]]):
        return
    data = ' '.join(jsondata)
    info:dict = json.loads(data)
    required = [
        'title',
        'name',
        'content'
    ]
    # for x in list(info.keys()):
    #     if x in required:
    #         required.remove(x)
    _ = [required.remove(x) for x in list(info.keys()) if x in required]
    if required:
        await ctx.send(f"Missing one or more required parameters: {' '.join(required)}")
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
