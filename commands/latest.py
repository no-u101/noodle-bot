#latest.py

import json
import discord
import requests

async def command(ctx):
    baseUrl = "https://api.github.com"
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    p = {
        "per_page": 1
    }
    r = requests.get(f"{baseUrl}/repos/Aeroluna/NoodleExtensions/releases", headers=headers, params=p)
    data = json.loads(r.text)[0]

    embed = (discord.Embed(title=data['name'], description=data['body'].replace('#', ''), color=discord.Color.blurple())
    .set_thumbnail(url=data['author']['avatar_url'])
    .add_field(name="Download", value=f'[Download {data["name"]}]({data["assets"][0]["browser_download_url"]})'))
    
    await ctx.send(embed=embed)