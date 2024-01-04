import os
from io import BytesIO

import requests
from PIL import Image
from discord.ext import commands
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
OFFICER_CHANNEL_ID = 1192356947094155356
VERIFY_CHANNEL_ID = 1192360611825324134

client = discord.Client(intents=discord.Intents.all())



@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    verify_channel = client.get_channel(VERIFY_CHANNEL_ID)
    officer_channel = client.get_channel(OFFICER_CHANNEL_ID)
    if message.author == client.user or message.channel != verify_channel:
        return

    if message.content == 'hello':
        print(officer_channel)
        await officer_channel.send(f'Hi {message.author}')
    elif message.content == 'bye':
        await officer_channel.send(f'Goodbye {message.author}')
    else:
        if message.attachments and len(message.attachments) == 1:
            # Get the image file
            image_file = message.attachments[0]

            # Read the image file content as bytes
            image_bytes = await image_file.read()

            # Send the image to the server channel
            await officer_channel.send(message.content, file=discord.File(fp=BytesIO(image_bytes), filename=image_file.filename))
        elif message.attachments and len(message.attachments) > 1:
            await officer_channel.send(message.content)
            for attachment in message.attachments:
                image_bytes = attachment.read()
                await officer_channel.send(file=discord.File(image_bytes))
        else:
            await officer_channel.send(message.content)


client.run(TOKEN)