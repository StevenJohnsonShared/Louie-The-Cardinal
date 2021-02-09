import os
import asyncio
import discord
from discord.ext import commands

client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('--------')
    print("hi")

@client.event
async def on_message(message):
    await client.process_commands(message)


client.run(os.environ['token'])