import discord
import os
import requests
import json
from data_store import data_store
from search_key import search
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!rarity'):
        store = data_store.get()
        id = message.content[8:]
        # GET REQUEST ON GIVEN ID
        resp = requests.get('https://api.ergoplatform.com/api/v1/tokens/'+id)
        initial = json.loads(resp.text)['description']
        data = json.loads(initial)
        score = (float(store['background'][search(None,data,"background")]) +
                float(store['facecolor'][search(None,data,"facecolor")]) +
                float(store['ears'][search(None,data,"ears")]) + 
                float(store['eyes'][search(None,data,"eyes")]) +
                float(store['body'][search(None,data,"body")]) +
                float(store['head'][search(None,data,"head")]) +
                float(store['nose'][search(None,data,"nose")]) +
                float(store['expression'][search(None,data,"expression")]))
        await message.channel.send(score)

# PUT TOKEN HERE
client.run(os.getenv('TOKEN'))