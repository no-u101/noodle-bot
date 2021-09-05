import os
import json
import discord
from discord import message
from discord.ext import commands
from importlib import import_module, reload

class ModLogger(commands.Cog):
    """A mod logger for all forms of action that happen in the server."""

    logs_channel:discord.TextChannel = None
    noodle_server:discord.Guild = None

    def __init__(self, bot):
        self.bot:commands.Bot = bot
    

    @commands.Cog.listener()
    async def on_message_edit(self, before:discord.Message, after:discord.Message):
        embed = discord.Embed(title='Message Edited', description=f'"{before.content}" -> "{after.content}"\nFrom: {after.author}\nIn: <#{after.channel.id}>', color=discord.Colour.blurple())
        await self.logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message:discord.Message):
        embed = discord.Embed(title='Message Deleted', description=f'"{message.content}"\nFrom: {message.author.nick}\nIn: <#{message.channel.id}>', color=discord.Colour.blurple())
        await self.logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member:discord.Member):
        await self.logs_channel.send(f'{member} left the server')
    
    @commands.Cog.listener()
    async def on_member_ban(self, guild:discord.Guild, user:discord.User):
        banLog:discord.AuditLogEntry = [x async for x in self.noodle_server.audit_logs(limit=1)][0] # I HATE THIS 
        
        embed = discord.Embed(title='Member Banned', description=f'{user} was banned.\nReason: {banLog.reason}\nBanned From: {banLog.user}', color=discord.Colour.red())
        await self.logs_channel.send(embed=embed)



class NoodleBot(commands.Cog):

    cmds = [x[:-3].lower() for x in os.listdir('./commands') if x.endswith('.py')]
    command_functions = [
        import_module(f'commands.{x[:-3]}') for x in os.listdir('./commands') if x.endswith('.py')
    ]

    
    def __init__(self, bot):
        self.bot:commands.Bot = bot

    async def update_commands(self):
        self.cmds = [x[:-3].lower() for x in os.listdir('./commands') if x.endswith('.py')]
        self.command_functions = [
            import_module(f'commands.{x[:-3]}') for x in os.listdir('./commands') if x.endswith('.py')
        ]

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} is online and usable.")
        await self.bot.change_presence(activity=discord.Game(name='Beat Saber Modcharts'))

        modLogger:ModLogger = self.bot.get_cog('ModLogger')
        modLogger.logs_channel = self.bot.get_channel(848645733553012766)
        modLogger.noodle_server = self.bot.get_guild(841467564089147434)

    @commands.Cog.listener()    
    async def on_message(self, message:discord.Message):
        
        if message.author.bot or message.author._user == self.bot.user:
            return
        
        if message.content.startswith("!") and message.channel.id == 876302444408233994: # make sure it's in #bot-spam
            # check if command exists
            command_used = message.content[1:].lower() # exclude !
            if command_used in self.cmds:
                # re-import the command.py file and execute it
                args = ()
                if len(message.content.split()) == 1:
                    args = ()
                else:
                    args = tuple(message.content.split()[1:])
                
                await self.update_commands()
                self.command_functions[self.cmds.index(command_used)] = reload(self.command_functions[self.cmds.index(command_used)])
                await self.command_functions[self.cmds.index(command_used)].command(await self.bot.get_context(message), *args)
                return

        await self.bot.process_commands(message)

bot = commands.Bot("!", case_insensitive=True, intents=discord.Intents.all())
bot.add_cog(NoodleBot(bot))
bot.add_cog(ModLogger(bot))
data = json.load(open('./data.json'))

bot.run(data['token'])