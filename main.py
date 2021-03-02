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

@client.command(name="hi-louie")
async def hello(context):
    await context.message.channel.send("hi")

# Delete Messages: !deleteMessages {number of messages}
# used to delete specific number of messages.
@client.command(name='deleteMessages')
async def deleteMessages(context):
    # get the content of the message and split the parameters from the command.
    content = context.message.content.split(' ')

    # If the length of the message is not two or the parameter is not numeric
    # then the command is not used correctly.
    if len(content) != 2 or not content[1].isnumeric():
        await context.message.channel.send("Incorrect usage of !deleteMessage. Example: !deleteMessage {number of messages}.")
        return

    # Get the channel that the message was sent in.
    channel = context.message.channel
    # Get the number of messages specified from the channel the message was sent in.
    fetchedMessages = await channel.history(limit=int(content[1])+1).flatten()

    # For each message fetched, delete.
    for messages in fetchedMessages:
        await messages.delete()
    

# Move: !move {channel to move to} {number of messages}
# Used to move messages from one channel to another.
@client.command(name='move')
async def move(context):

    if "Officers" not in [y.name.lower() for y in context.message.author.roles]:
        await context.message.delete()
        await context.channel.send("{} you do not have the permissions to move messages.".format(context.message.author))
        return

    # get the content of the message
    content = context.message.content.split(' ')
    # if the length is not three the command was used incorrectly
    if len(content) != 3 or not content[2].isnumeric():
        await context.message.channel.send("Incorrect usage of !move. Example: !move {channel to move to} {number of messages}.")
        return
    # channel that it is going to be posted to
    channelTo = content[1]
    # get the number of messages to be moved (including the command message)
    numberOfMessages = int(content[2]) + 1
    # get a list of the messages
    fetchedMessages = await context.channel.history(limit=numberOfMessages).flatten()
    
    # delete all of those messages from the channel
    for i in fetchedMessages:
        await i.delete()

    # invert the list and remove the last message (gets rid of the command message)
    fetchedMessages = fetchedMessages[::-1]
    fetchedMessages = fetchedMessages[:-1]

    # Loop over the messages fetched
    for messages in fetchedMessages:
        # get the channel object for the server to send to
        channelTo = discord.utils.get(messages.guild.channels, name=channelTo)

        # if the message is embeded already
        if messages.embeds:
            # set the embed message to the old embed object
            embedMessage = messages.embeds[0]
        # else
        else:
            # Create embed message object and set content to original
            embedMessage = discord.Embed(
                        description = messages.content
                        )
            # set the embed message author to original author
            embedMessage.set_author(name=messages.author, icon_url=messages.author.avatar_url)
            # if message has attachments add them
            if messages.attachments:
                for i in messages.attachments:
                    embedMessage.set_image(url = i.proxy_url)

        # Send to the desired channel
        await channelTo.send(embed=embedMessage)


client.run(os.environ['token'])
