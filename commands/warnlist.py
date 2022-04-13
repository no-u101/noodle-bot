from discord.ext.commands import Context
import datetime
import discord
import json

async def command(ctx:Context, uid):
    if not any([y in "administrator staff founder" for y in [x.name.lower() for x in ctx.author.roles]]):
        return
    try:
        int(uid)
    except ValueError:
        await ctx.send("That's not a UID")
    
    warns:dict = json.load(open("./warns.json", encoding='utf-8'))
    user = ctx.guild.get_member(int(uid))
    
    if warns.get(uid):
        embed = discord.Embed(title=f"{user}'s warns", description=f"<@{uid}>", color=discord.Color.blurple())
        for x in warns[uid]:
            date = datetime.datetime.fromtimestamp(int(x['date']))
            embed.add_field(name=f'{date} (UTC)', value=f"warned by <@{x['caller']}>: `{x['reason']}`\n", inline=False)
            
        await ctx.send(embed=embed)
    else:
        await ctx.send("That user has not been warned")