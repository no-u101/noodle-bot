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
allCommandsContext = [
    open(f"./commands/{x}").read() for x in os.listdir("./commands/") if os.path.isfile(f"./commands/{x}")
]

async def sendMessage(channelID, **args):
    oauth = {
        "Authorization": f"Bot {data['token']}"
    }
    url = f"https://discord.com/api/v8/channels/{channelID}/messages"

    r = requests.post(url, headers=oauth, json=args)

    print(r.text)

def isListOfWordsInString(words, string, maxMatch=1, substractOnNotMatching=False):
    matches = 0
    for x in words:
        if x in string:
            matches += 1
        else:
            if substractOnNotMatching:
                matches -= 1
    return matches >= maxMatch

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Beat Saber Modcharts"))
    print("bot is ready")

@bot.command()
@cmds.has_any_role("Founder", "Moderator", "Staff")
async def refreshCommands(ctx:cmds.Context):
    global allCommands
    global allCommandsContext

    if os.sys.platform == "win32":
        os.system("rmdir /Q /S .\\commands\\__pycache__")
    else:
        os.system("rm -rf ./commands/__pycache__")

    diff = """```diff
"""
    for x in allCommands:
        try:
            reload(x)
        except:
            pass

    filesChanged = []
    for x in allCommandsContext:
        if not x.startswith("#"):
            filesChanged.append(1)
            continue
            
        fileItem = x.splitlines()[0][1:]
        if os.path.exists(f"./commands/{fileItem}"):
            fileContent = open(f"./commands/{fileItem}").read()
            filesChanged.append(fileContent)
        else:
            filesChanged.append(0)

    if len([x for x in os.listdir("./commands/") if os.path.isfile(f"./commands/{x}")]) > len(filesChanged):
        for newCommand in [x for x in os.listdir("./commands/") if os.path.isfile(f"./commands/{x}")]:
            newCommandFile = open(f'./commands/{newCommand}').read()
            if newCommandFile not in filesChanged:
                if newCommandFile.startswith("#"):
                    diff += f"+ new command commands.{newCommandFile.splitlines()[0][1:].split('.')[0]}\n"
                else:
                    diff += f"- /!\\ error detected in new command {allCommands[x].__name__}: file supposed to start with #(filename)\n"


    for x in range(len(filesChanged)):
        if x == len(allCommandsContext):
            break
        
        if filesChanged[x] == 0:
            diff += f"- command {allCommands[x].__name__} removed\n"
        elif filesChanged[x] == 1:
            diff += f"- /!\\ error detected in changed command {allCommands[x].__name__}: file supposed to start with #(filename). (If it was fixed, make sure to reload again for this change to take effect.)\n"
        else:
            charDiffCount = len(filesChanged[x]) - len(allCommandsContext[x])
            if charDiffCount < 0:
                diff += f"- {abs(charDiffCount)} removals on {allCommands[x].__name__}\n"
            elif charDiffCount > 0:
                diff += f"+ {charDiffCount} additions on {allCommands[x].__name__}\n"
    diff += "```"
    allCommands = [
        import_module(f"commands.{x.split('.')[0]}") for x in os.listdir("./commands/") if os.path.isfile(f"./commands/{x}")
    ]

    allCommandsContext = [
        open(f"./commands/{x}").read() for x in os.listdir("./commands/") if os.path.isfile(f"./commands/{x}")
    ]
    if diff == "```diff\n```":
        await ctx.send("Refreshed commands, nothing changed.")
    else:
        await ctx.send(f"Refreshed commands, here's what changed: {diff}")

@bot.event
async def on_message(message:discord.Message):

    if message.author.bot or message.author._user == bot.user:
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
    
    # FAQ area
    if isListOfWordsInString("started start noodle extensions".split(), message.content.lower(), 3):
        await message.channel.send("**How do I get started making Noodle Extensions levels?**\nYou can check out <#847956650090168330>. It explains in as much detail as possible how you can get started. If you have any questions remaining after reading it, feel free to ask!")
        return
    elif isListOfWordsInString("give have can get want".split(), message.content.lower()):
        if isListOfWordsInString("admin mod moderator".split(), message.content.lower()):
            await message.channel.send("No you will not get mod perms.")

    await bot.process_commands(message)


bot.run(data['token'])