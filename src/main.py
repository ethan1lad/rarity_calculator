"""Main Discord Bot Runtime"""

import json
import os
import csv
import discord
import requests
from data_store import Datastore
from search_key import search

client = discord.Client()
data_store = Datastore()


@client.event
async def on_ready():
    """Respond to discord ready event"""
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    """Respond to discord message event"""
    if message.author == client.user:
        return

    if message.content.startswith('!rarity'):
        store = data_store.get()
        token_id = message.content[8:]
        # GET REQUEST ON GIVEN ID
        resp = requests.get('https://api.ergoplatform.com/api/v1/tokens/' + token_id)
        initial = json.loads(resp.text)['description']
        data = json.loads(initial)
        score = (float(store['background'][search(None, data, "background")]) +
                 float(store['facecolor'][search(None, data, "facecolor")]) +
                 float(store['ears'][search(None, data, "ears")]) +
                 float(store['eyes'][search(None, data, "eyes")]) +
                 float(store['body'][search(None, data, "body")]) +
                 float(store['head'][search(None, data, "head")]) +
                 float(store['nose'][search(None, data, "nose")]) +
                 float(store['expression'][search(None, data, "expression")]))
        await message.channel.send("Rarity Score is " + str(score))

    if message.content.startswith('!rank #'):
        token_id = message.content[6:]
        no_hash = token_id[1:].lstrip('0')
        if int(no_hash) < 10:
            token_id = '#000' + no_hash
        elif int(no_hash) < 100:
            token_id = '#00' + no_hash
        elif int(no_hash) < 1000:
            token_id = '#0' + no_hash
        with open('../data/ranks2.csv', "r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                data_id = row[0][:5]
                if token_id in data_id:
                    rank = row[-1]
                    await message.channel.send(data_id + " has rank " + str(rank) + "/3000")


# PUT TOKEN HERE
client.run(os.getenv('TOKEN'))
