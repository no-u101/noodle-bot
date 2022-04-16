import asyncio
import os
import json
import discord
from discord.ext import commands
from importlib import import_module, reload

#region ModLogger
class ModLogger(commands.Cog):
    """A mod logger for all forms of action that happen in the server."""

    logs_channel:discord.TextChannel = None
    noodle_server:discord.Guild = None

    def __init__(self, bot):
        self.bot:commands.Bot = bot

    @staticmethod     
    def admin_staff(message: discord.Message):
        return any([discord.utils.get(message.author.roles, name="Administrator"), 
                    discord.utils.get(message.author.roles, name="Staff")]
                )
    
    @commands.Cog.listener()
    async def on_message_edit(self, before:discord.Message, after:discord.Message):
        if before.content == after.content or after.author == self.bot.user or after.channel.id == 890689165442809888: # if self-edit / emb update
            return
        embed = discord.Embed(title='Message Edited', description=f'"{before.content}" -> "{after.content}"\nFrom: {after.author}\nIn: <#{after.channel.id}>', color=discord.Colour.blurple())
        await self.logs_channel.send(embed=embed)
        

        if (not self.admin_staff(after)) and (not discord.utils.get(after.author.roles, name='Support')):
            invite = "discord.gg/"
            if invite in after.content:
                await after.channel.send(f"<@{after.author.id}> invites are not allowed")
                await after.delete()

                    
    @commands.Cog.listener()
    async def  on_raw_message_delete(self, message):
        if message.channel_id != 890689165442809888:
            if message.cached_message:
                embed = discord.Embed(title='Message Deleted', description=f'"{message.cached_message.content}"\nFrom: {message.cached_message.author}\nIn: <#{message.channel_id}>', color=discord.Colour.blurple())
                if len(message.attachments) != 0:
                    embed.add_field(name='The following image was attached:', value=f'{message.attachments[0].filename}')
                    embed.set_image(url=message.attachments[0].url)
                await self.logs_channel.send(embed=embed)
            else:
                embed = discord.Embed(title='Message Deleted', description=f'Message content unknown.\nFrom: unknown.\nIn: <#{message.channel_id}>', color=discord.Colour.blurple())
                if len(message.attachments) != 0:
                    embed.add_field(name='Images', value=f'{message.attachments[0].filename}')
                    embed.set_image(url=message.attachments[0].url)
                await self.logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member:discord.Member):
        await self.logs_channel.send(f'{member} left the server')
    
    @commands.Cog.listener()
    async def on_member_ban(self, guild:discord.Guild, user:discord.User):
        banLog:discord.AuditLogEntry = list(self.noodle_server.audit_logs(limit=1))[0] # i hate this less than before
        
        embed = discord.Embed(title='Member Banned', description=f'{user} was banned.\nReason: {banLog.reason}\nBanned From: {banLog.user}', color=discord.Colour.red())
        await self.logs_channel.send(embed=embed)
#endregion

#region Main Bot Command Handling
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

    async def statusLoop(self):
        while True:
            await self.bot.change_presence(activity=discord.Activity(name='your DM reports', type=discord.ActivityType.listening))
            await asyncio.sleep(30)
            await self.bot.change_presence(activity=discord.Game(name='Beat Saber Modcharts'))
            await asyncio.sleep(30)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} is online and usable.\n{self.cmds}")
        modLogger:ModLogger = self.bot.get_cog('ModLogger')
        modLogger.logs_channel = self.bot.get_channel(848645733553012766)
        modLogger.noodle_server = self.bot.get_guild(841467564089147434)
        await self.statusLoop()

    @commands.Cog.listener()    
    async def on_message(self, message:discord.Message):
        
        if message.author.bot or message.author == self.bot:
            return

        if message.content.startswith("!"):
            await self.update_commands()
            # check if command exists
            command_used = message.content.split()[0][1:].lower() # exclude !
            print(command_used)
            if command_used in self.cmds:
                # re-import the command.py file and execute it
                args = ()
                if len(message.content.split()) == 1:
                    args = ()
                else:
                    args = tuple(message.content.split()[1:])
                
                self.command_functions[self.cmds.index(command_used)] = reload(self.command_functions[self.cmds.index(command_used)])
                await self.command_functions[self.cmds.index(command_used)].command(await self.bot.get_context(message), *args)
                return

        # prevent code below from being run if user is an admin. this means anything below will be accessible to admin only.
        if not ModLogger.admin_staff(message):
            
            if "discord.gg/" in message.content and not discord.utils.get(message.author.roles, name='Support'):
                await message.channel.send(f"<@{message.author.id}> no invites are allowed in this server.")
                await message.delete()
                return

        await self.bot.process_commands(message)
#endregion

#region DMReport
class DMReport(commands.Cog):

    def __init__(self, bot):
        self.bot:commands.Bot = bot

        

    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):

        reportChannel = self.bot.get_channel(891083452995223582)
        
        if message.author == self.bot.user:
            return
        
        if str(message.channel.type) == "private":
            emb = (discord.Embed(title="Report", color=discord.Color.blurple())
                    .add_field(name='Reporter', value=message.author, inline=False)
                    .add_field(name='Contents', value=message.content, inline=False))
            if len(message.attachments) != 0:
                emb.add_field(name='The following image was attached:', value=f'{message.attachments[0].filename}')
                emb.set_image(url=message.attachments[0].url)
            
            await reportChannel.send(embed=emb)
            await message.author.send("Thank you for your report! It has been recorded and the moderation team will look at it shortly.")
            
#endregion


intents = discord.Intents.all()

bot = commands.Bot("!", case_insensitive=True, intents=intents, help_command=None)

bot.add_cog(NoodleBot(bot))
bot.add_cog(DMReport(bot))
bot.add_cog(ModLogger(bot))

data = json.load(open('./data.json', encoding='utf-8'))

bot.run(data['token'])
