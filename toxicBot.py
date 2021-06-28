import discord
import json
import math
import os
from googleapiclient import discovery
import pymongo
from pymongo import MongoClient
from pymongo import ReturnDocument
from dotenv import load_dotenv

import db_imports
load_dotenv()

conn_username = os.getenv('CONN_USERNAME')
conn_password = os.getenv('CONN_PASSWORD')
conn_string = f"mongodb+srv://{conn_username}:{conn_password}@toxicbot.cgrie.mongodb.net/toxic_database?retryWrites=true"

client = MongoClient(conn_string)
db = client.toxic_database
usersToxicity = db.usersToxicity #collection of users' toxicity levels

discordClient = discord.Client()

perspective_client = discovery.build(
    "commentanalyzer",
    "v1alpha1",
    developerKey=os.getenv('API_KEY'),
    discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
    static_discovery=False,
)

@discordClient.event
async def on_ready():
    print('We have logged in as {0.user}'.format(discordClient))

@discordClient.event
async def on_message(message):
    if message.author == discordClient.user:
        return

    toxicityAvg = messageCount = toxicScore = 0

    toxicScore = db.usersToxicity.find_one({'user': message.author.id})

    try:
        if message.content.startswith('$toxicscore'):
            await message.channel.send(f"You have sent {toxicScore['messageCount']} messages with a "
                                       f"toxicity score of {round(toxicScore['toxicityAvg'], 2)}")
            return
    except:
        await message.channel.send('You need to chat before you can have a toxicity score')
        return

    analyze_request = {
      'comment': { 'text': message.content},
      'requestedAttributes': {'TOXICITY': {}}
    }

    response = perspective_client.comments().analyze(body=analyze_request).execute()

    print(response)

    perspective_response = response['attributeScores']['TOXICITY']['spanScores'][0]['score']['value']

    toxicityScore = perspective_response * 100

    print(f"{message.author.display_name} said: {message.content}\" and it had a toxicity score of: "
          f"{toxicityScore}")

    curToxicity = db.usersToxicity.find_one_and_update(
        {'user': message.author.id},
        {'$inc': {'messageCount': 1,
                  'toxicSum': toxicityScore}},
        upsert = True,
        return_document = ReturnDocument.AFTER)

    messageCount = curToxicity['messageCount']
    toxicSum = curToxicity['toxicSum']

    toxicityAvg = toxicSum / messageCount

    #update userToxicity in db with new toxicityAvg
    db.usersToxicity.find_one_and_update(
        {'user': message.author.id},
        {'$set': {'toxicityAvg': toxicityAvg}},
        upsert = True)

discordClient.run(os.getenv('TOKEN'))
