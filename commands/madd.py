#madd.py

import json
import discord
from discord.ext import commands


async def command(ctx:commands.Context, name:str, title:str, *content:str): # star because every single word and shit will be seperated
    if not any([y in "support" for y in [x.name.lower() for x in ctx.author.roles]]):
        return

    macros = json.load(open('./macros.json'))
    macros[name] = {
        "title":title,
        "content":' '.join(content)
    }
    json.dump(macros, open('./macros.json', 'w', encoding='utf-8'))
