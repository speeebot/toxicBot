import discord
import json
import math
import os
from googleapiclient import discovery
from dotenv import load_dotenv

load_dotenv()

discordClient = discord.Client()

client = discovery.build(
  "commentanalyzer",
  "v1alpha1",
  developerKey=os.getenv('API_KEY'),
  discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
  static_discovery=False,
)

toxicityAvg = messageCount = 0

@discordClient.event
async def on_ready():
    print('We have logged in as {0.user}'.format(discordClient))

@discordClient.event
async def on_message(message):
    if message.author == discordClient.user:
        return

    if message.content.startswith('$toxicscore'):
        await message.channel.send('Your toxicity score is ')

    global toxicityAvg, toxicityScore
   # await message.channel.send(message.content)
    analyze_request = {
      'comment': { 'text': message.content},
      'requestedAttributes': {'TOXICITY': {}}
    }

    response = client.comments().analyze(body=analyze_request).execute()
    print(response)

    toxicityScore = math.floor(response['attributeScores']['TOXICITY']['spanScores'][0]['score']['value'] * 100)
    print(toxicityScore)

    if toxicityScore in range(95, 100):
        await message.channel.send('TOXIC LEVEL 9000!')
    elif toxicityScore in range(90, 95):
        await message.channel.send('That was pretty toxic.')
    elif toxicityScore in range(80, 90):
        await message.channel.send('Not bad.')
    elif toxicityScore in range(70, 80):
        await message.channel.send('Try again.')

discordClient.run(os.getenv('TOKEN'))
