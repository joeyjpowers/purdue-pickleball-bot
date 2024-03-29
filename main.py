import os
from io import BytesIO

import mysql.connector
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
        if message.attachments:
            files_to_send = []
            for attachment in message.attachments:
                # Get the image file
                image_file = attachment

                # Read the image file content as bytes
                image_bytes = await image_file.read()
                files_to_send.append(discord.File(fp=BytesIO(image_bytes), filename=image_file.filename))

                # Send the image to the server channel
            await officer_channel.send(f"{message.content} ({message.author})", files=files_to_send)
        else:
            await officer_channel.send(f"{message.content} ({message.author})")


@client.event
async def on_reaction_add(reaction, user):
    print(reaction.emoji)
    print(reaction.message.content)
    print(user)
    if reaction.emoji == "✅":
        print("check mark")
    elif reaction.emoji == "❌":
        print("x")
    await reaction.message.channel.send(f'{user} reacted with {reaction.emoji}')


client.run(TOKEN)
