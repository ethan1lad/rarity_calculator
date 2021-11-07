"""Main Discord Bot Runtime"""

import json
import os
import csv
import discord
import requests
from data_store import Datastore
from helpers import search, clean_gnome_id
import random

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
        gnome_id = message.content[8:]
        # GET REQUEST ON GIVEN ID
        resp = requests.get('https://api.ergoplatform.com/api/v1/tokens/' + gnome_id)
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
        gnome_id = message.content[6:]
        gnome_id = clean_gnome_id(gnome_id)
        with open('../data/ranks2.csv', "r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                data_id = row[0][:5]
                if gnome_id in data_id:
                    rank = row[-1]
                    await message.channel.send(data_id + " has rank " + str(rank) + "/3000")


    if message.content.startswith('!details #'):
        gnome_id = message.content[9:]
        gnome_id = clean_gnome_id(gnome_id)
        with open('../data/ranks2.csv', "r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                data_id = row[0][:5]
                if gnome_id in data_id:
                    token_id = row[-2]
                    # GET REQUEST ON GIVEN ID
                    resp = requests.get('https://api.ergoplatform.com/api/v1/tokens/' + token_id)
                    box_id = json.loads(resp.text)['boxId']
                    resp1 = requests.get('https://api.ergoplatform.com/api/v1/boxes/' + box_id)
                    data = json.loads(resp1.text)['additionalRegisters']['R9']['renderedValue']
                    image_url = bytes.fromhex(data).decode("ASCII")
                    embed = discord.Embed(title=f"Gnomekin ID: {gnome_id}",
                                          description=f" Rank: {row[-1]}/3000\n  Rarity Score: {round(float(row[-3]),3)} \n Token Id: {token_id}\n ",
                                          color=0xFF5733)
                    embed.set_image(url=image_url)
            await message.channel.send(embed=embed)


    if message.content.startswith('!random'):
        gnome_id = '#'+str(random.randint(1,3000))
        gnome_id = clean_gnome_id(gnome_id)
        with open('../data/ranks2.csv', "r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                data_id = row[0][:5]
                if gnome_id in data_id:
                    token_id = row[-2]
                    # GET REQUEST ON GIVEN ID
                    resp = requests.get('https://api.ergoplatform.com/api/v1/tokens/' + token_id)
                    box_id = json.loads(resp.text)['boxId']
                    resp1 = requests.get('https://api.ergoplatform.com/api/v1/boxes/' + box_id)
                    data = json.loads(resp1.text)['additionalRegisters']['R9']['renderedValue']
                    image_url = bytes.fromhex(data).decode("ASCII")
                    embed = discord.Embed(title=f"Gnomekin ID: {gnome_id}",
                                          description=f" Rank: {row[-1]}/3000\nRarity Score: {round(float(row[-3]),3)} \nToken Id: {token_id}\n ",
                                          color=0xFF5733)
                    embed.set_image(url=image_url)
            await message.channel.send(embed=embed)

    if message.content.startswith('!issue'):
        if len(message.content) < 20:
            await message.channel.send('Please submit a token ID!')
        else:
            with open('issues.txt', 'a') as file:
                file.write(message.content + '\n')
                await message.channel.send('Issue submitted, thanks!')





# PUT TOKEN HERE
client.run(os.getenv('TOKEN'))
