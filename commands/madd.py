#madd.py

import json
import discord
from discord.ext import commands


async def command(ctx:commands.Context, *jsondata): # star because every single word and shit will be seperated
    if not any([y in "support" for y in [x.name.lower() for x in ctx.author.roles]]):
        return
    data = ' '.join(jsondata)
    info = json.loads(data)
    name = info['name']
    title = info['title']
    content = info['content']

    macros = json.load(open('./macros.json'))
    if name in macros.keys():
        await ctx.send("That macro already exists.")
        return
    macros[name] = {
        "title":title,
        "content":content
    }
    json.dump(macros, open('./macros.json', 'w', encoding='utf-8'))
    await ctx.send("Success adding macro.")
