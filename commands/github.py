#github.py
async def command(ctx):
    if len(ctx.author.roles) >= 1:
        await ctx.send("**Thank you for your contribution!**\nhttps://github.com/megamaz/noodle-bot")