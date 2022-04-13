from discord.ext.commands import Context
import json
import time

async def command(ctx:Context, uid, *reason):
    if not any([y in "administrator staff founder" for y in [x.name.lower() for x in ctx.author.roles]]):
        return
    reason = ' '.join(reason)
    try:
        int(uid)
    except ValueError:
        await ctx.send("That's not a UID")
    
    warns:dict = json.load(open("./warns.json", encoding='utf-8'))
    warn = {
        "reason":reason,
        "caller":ctx.author.id,
        "date":str(int(time.time()))
    }
    if warns.get(uid):
        warns[uid].append(warn)
    else:
        warns[uid] = [warn]
    
    json.dump(warns, open("./warns.json", 'w', encoding='utf-8'))
    user = ctx.guild.get_member(int(uid))
    await ctx.send(f"Warned {user} for '{reason}'")