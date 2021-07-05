import os
import json
import asyncio
import discord
import requests
from importlib import import_module, reload
from discord.ext import commands as cmds

data = json.load(open("./data.json"))

bot = cmds.Bot("NE!", None, case_insensitive=True)

allCommands = [
    import_module(f"commands.{x.split('.')[0]}") for x in os.listdir("./commands/") if os.path.isfile(f"./commands/{x}")
]

async def sendMessage(channelID, **args):
    oauth = {
        "Authorization": f"Bot {data['token']}"
    }
    url = f"https://discord.com/api/v8/channels/{channelID}/messages"

    r = requests.post(url, headers=oauth, json=args)

    print(r.text)

@bot.event
async def on_ready():
    print("bot is ready")

@bot.command()
@cmds.has_any_role("Founder", "Moderator", "Staff")
async def refreshCommands(ctx:cmds.Context):
    global allCommands

    if os.sys.platform == "win32":
        os.system("rmdir /Q /S .\\commands\\__pycache__")
    else:
        os.system("rm -rf ./commands/__pycache__")

    for x in allCommands:
        reload(x)      

    allCommands = [
        import_module(f"commands.{x.split('.')[0]}") for x in os.listdir("./commands/") if os.path.isfile(f"./commands/{x}")
    ]

    await ctx.send("Refreshed commands.")

@bot.event
async def on_message(message:discord.Message):

    if message.author.bot or message.author == bot.user:
        return

    if message.content.startswith("NE!"):
        commandsAsStrList = [(x.__name__).lower() for x in allCommands]
        command = f"commands.{message.content.split()[0].split('!')[1]}".lower()

        if command in commandsAsStrList:
            args = []
            if len(message.content.split()) == 1:
                args = ()
            else:
                args = tuple(message.content.split()[1:])
            await allCommands[commandsAsStrList.index(command)].command(await bot.get_context(message), *args)
    
            return
    
    await bot.process_commands(message)


bot.run(data['token'])