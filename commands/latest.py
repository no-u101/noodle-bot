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
    noodle_extension = requests.get(f"{baseUrl}/repos/Aeroluna/NoodleExtensions/releases", headers=headers, params=p)
    data_ne = json.loads(noodle_extension.text)[0]

    custom_json_data = requests.get(f"{baseUrl}/repos/Aeroluna/CustomJSONData/releases", headers=headers, params=p)
    data_cjd = json.loads(custom_json_data.text)[0]

    heck = requests.get(f"{baseUrl}/repos/Aeroluna/Heck/releases", headers=headers, params=p)
    data_heck = json.loads(heck.text)[0]

    embed = (discord.Embed(title=data_ne['name'], description=data_ne['body'].replace('#', ''), color=discord.Color.blurple())
    .set_thumbnail(url=data_ne['author']['avatar_url'])
    .add_field(name="Downloads", value=f'''[Download NE{data_ne["name"]}]({data_ne["assets"][0]["browser_download_url"]})
[Download CJD{data_cjd["name"]}]({data_cjd["assets"][0]["browser_download_url"]})
[Download Heck{data_heck["name"]}]({data_heck["assets"][0]["browser_download_url"]})'''))
    
    await ctx.send(embed=embed)
