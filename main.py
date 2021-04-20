import os
import asyncio
import discord
import datetime
from discord.ext import commands

client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('--------')
    print("hi")

client.calendar = ['last']


@client.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.channels, name = 'general')
    await channel.send('{} has left the server'.format(member))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.author.bot:
        return
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
    # roles = [y.name.lower() for y in context.message.author.roles]
    # await asyncio.sleep(1)
    # if "officers" not in roles:
    #     await context.message.delete()
    #     await context.channel.send("{} you do not have the permissions to move messages.".format(context.message.author))
    #     return

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
    # get the channel object for the server to send to
    channelTo = discord.utils.get(fetchedMessages[0].guild.channels, name=channelTo)

    # Loop over the messages fetched
    for messages in fetchedMessages:
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


# Role Select: !role
# Allows people to select three roles before deleting the message. This can be useful for not
# only assigning roles in the server, but maybe minigames hosted in the discord server.
@client.command(name = "role")
async def role(context):
    msg = await context.message.channel.send("select role")
    reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
    dictionary = {
           '1️⃣' : 'among',
           '2️⃣' : 'cod',
           '3️⃣' : 'csgo',
           '4️⃣' : 'hearthstone',
           '5️⃣' : 'league',
           '6️⃣' : 'magic',
           '7️⃣' : 'minecraft',
           '8️⃣' : 'overwatch',
           '9️⃣' : 'rainbowsix',
           '🔟' : 'rocketleague'
           }
    for emoji in reactions:
        await msg.add_reaction(emoji)
    await asyncio.sleep(1)
    for i in range(3):
        reaction, user = await client.wait_for('reaction_add', timeout=60.0)
        emoji = reaction.emoji
        role = discord.utils.get(context.message.guild.roles, name = dictionary[emoji])
        await user.add_roles(role)
    msg.delete()

# Call Survey: !survey {Topic} optional: {question}, {parameter1}, {parameter2}, {parameter3}, {parameter4}
# Allows for someone to call a survey. If you choose to ask a question you MUST pass 4 parameters seperated
# by a space and a comma. Once the survey is over the person who called it will get a dm.
@client.command (name ='survey,')
async def survey(context):   # gets contents of message
    content = context.message.content.split(",") #splits message into array using commas
    if len(content) == 1:
        msg = await context.channel.send("Inproper use of Survey. !survey {topic} {optional question}")
        return
    if len(content) == 2: 
        subject = content[1]
        msg = await context.message.channel.send("Survey on {}, are you pro or con?".format(subject))
        reactions = ["\N{THUMBS UP SIGN}", "\N{THUMBS DOWN SIGN}"]

    elif len(content) > 2: 
        subject = content[1]
        question = content[2]
        option1 = content[3]
        option2 = content[4]
        option3 = content[5]
        option4 = content[6]
        option5 = "Other"
        msg = await context.message.channel.send("Survey on{}. The question is{}, \n1. {} \n2. {} \n3. {} \n4. {} \n5. {}".format(subject,question,option1,option2,option3,option4,option5))
        reactions = ["1️⃣", "2️⃣","3️⃣","4️⃣","5️⃣"] # adds emojis to allow users to vote

    for emojis in reactions:
      await msg.add_reaction(emojis)
    await asyncio.sleep(3)
    await context.channel.send("Finished sleeping, Survey is over! \nLook at the reactions for the results!")
    member = context.message.author
    await member.send("Your survey has finished in ({}).({}).".format(context.guild, context.channel))


#Schedule Event: -schedule {date} {time} {title} 
# Used to scheule events into the calendar
@client.command(name='schedule')
async def schedule(context):

    # get the content of the message and split the parameters from the command.
    content = context.message.content.split(' ')

    if len(content) < 4:
        await context.message.channel.send("Incorrect usage of -schedule. Example: -schedule {date (MM/DD/YYYY)} {time (HH:MM AM/PM)} {title}")
        return
    # separates date format into seperate values in date array
    date = content[1].split('/')
    # changes date values into int for datetime
    for x in range(len(date)):
        date[x] = int(date[x])
    # checks if valid date
    if date[0]>12 or date[0]<1 or date[1]>31 or date[1]<1 or date[2]<1000:
        await context.message.channel.send("Invalid date for -schedule. Example: -schedule {date (MM/DD/YYYY)} {time (HH:MM AM/PM)} {title}")
        return
    # separates time format into separate values in time array
    time = content[2].split(':')
    # changes time values into int for datetime
    for x in range(len(time)):
        time[x] = int(time[x])
    #adds am/pm values to time array
    time.append(content[3])
    # checks if am/pm values are correct
    if time[2].upper() != 'AM' and time[2].upper() != 'PM':
        await context.message.channel.send("Invalid time for -schedule. Example: -schedule {date (MM/DD/YYYY)} {time (HH:MM AM/PM)} {title}")
        return
    # takes the rest of content and adds it to title array
    title = []
    for x in range (4,len(content)):
        title.append(content[x])
    # changes time into 24 hour format for datetime
    if time[2].upper() == 'PM' and not time[0] == 12:
        time[0]+=12
    elif time[2].upper() == 'AM' and time[0] == 12:
        time[0]-=12
    # combines date and time into one datetime value
    eventDateTime = datetime.datetime(date[2],date[0],date[1],time[0],time[1])
    # combines all title strings into one string
    eventTitle = ' '.join(title)
    # combines datetime and title into a dictionary value to add to schedule
    event = {'date': eventDateTime, 'title': eventTitle}

    position = 0  
    # event insertion, sorted by date
    for x in range(len(client.calendar)):
        # if this position is empty, no date is earlier in the schedule, insert the event at this positon, leave for loop after
        if client.calendar[x] == 'last':
            client.calendar.insert(x, event) 
            position = x
            break
        # if this position in the schedule's date is earlier than the event's, insert the event at this position, leave for loop after
        elif client.calendar[x].get('date')>event.get('date'):
            client.calendar.insert(x, event)
            position = x
            break

    time[0]-=12
    if client.calendar[position].items() == event.items():
        await context.message.channel.send("Event has been added to calendar.")
    else:
        await context.message.channel.send("Failed to add event correctly. Please remove the event using -unschedule.")


#Request Calendar: !calendar {start date} {end date}
# Used to request all events in the calendar from start date to end date
@client.command(name='calendar')
async def calendar(context):

    # get the content of the message and split the parameters from the command.
    content = context.message.content.split(' ')

    # if no date is given
    if len(content) == 1:
        for i in range(len(client.calendar)-1):
            responseHold = client.calendar[i].get("date").strftime("%m")+'/'+client.calendar[i].get("date").strftime("%d")+'/'+client.calendar[i].get("date").strftime("%y")+' at '+ client.calendar[i].get("date").strftime("%I")+':'+client.calendar[i].get("date").strftime("%M")+client.calendar[i].get("date").strftime("%p")+' - '+client.calendar[i].get("title")
            await context.message.channel.send(responseHold)

    #if one date is given (assumed end date)
    elif len(content) == 2:
        # separates date format into seperate values in date array
        date = content[1].split('/')
        # changes date values into int for datetime
        for x in range(len(date)):
            date[x] = int(date[x])
        endDate = datetime.datetime(date[2], date[0], date[1])
        for i in range(len(client.calendar)-1):
            if client.calendar[i].get("date") > endDate:
                break
            responseHold = client.calendar[i].get("date").strftime("%m")+'/'+client.calendar[i].get("date").strftime("%d")+'/'+client.calendar[i].get("date").strftime("%y")+' at '+ client.calendar[i].get("date").strftime("%I")+':'+client.calendar[i].get("date").strftime("%M")+client.calendar[i].get("date").strftime("%p")+' - '+client.calendar[i].get("title")
            await context.message.channel.send(responseHold)

    #if two dates are given
    elif len(content) == 3:
        # separates date format into seperate values in date array
        date = content[1].split('/')
        # changes date values into int for datetime
        for x in range(len(date)):
            date[x] = int(date[x])
        startDate = datetime.datetime(date[2], date[0], date[1])
        # separates date format into seperate values in date array
        date = content[2].split('/')
        # changes date values into int for datetime
        for x in range(len(date)):
            date[x] = int(date[x])
        endDate = datetime.datetime(date[2], date[0], date[1])
        for i in range(len(client.calendar)-1):
            if client.calendar[i].get("date") >= startDate and client.calendar[i].get("date") <= endDate:
                responseHold = client.calendar[i].get("date").strftime("%m")+'/'+client.calendar[i].get("date").strftime("%d")+'/'+client.calendar[i].get("date").strftime("%y")+' at '+ client.calendar[i].get("date").strftime("%I")+':'+client.calendar[i].get("date").strftime("%M")+client.calendar[i].get("date").strftime("%p")+' - '+client.calendar[i].get("title")
                await context.message.channel.send(responseHold)

    else:
        await context.message.channel.send('Incorrect usage for -calendar. Example: -calendar {start date} {end date} for a range or -calendar for the entire calendar')

#Delete Event: -unschedule {title}
# Used to remove an event from the calendar
@client.command(name='unschedule')
async def unschedule(context):

    # get the content of the message and split the parameters from the command.
    content = context.message.content.split(' ')

    if not len(content) >= 2:
        await context.message.channel.send('Incorrect usage for -unschedule. Example: -unschedule {title}')
        return

    # sets title given in command to variable
    title = []
    for x in range(1,len(content)):
        title.append(content[x])
    title = ' '.join(title)

    #variable for error handling
    check = 0
    #search calendar for event
    for x in range(len(client.calendar)-1):
        if client.calendar[x] == 'last':
            break
        elif client.calendar[x].get("title") == title:
            client.calendar.pop(x)
            check = 1
    if check == 1:
        await context.message.channel.send('Deleted Event.')
    else:
        await context.message.channel.send('No event with that title found.')

#Reschedule Event: !reschedule {new date} {new time} {title}
# Used to reschedule an event already in the calendar
@client.command(name='reschedule')
async def reschedule(context):

    # get the content of the message and split the parameters from the command.
    content = context.message.content.split(' ')

    if len(content) < 4:
        await context.message.channel.send("Incorrect usage of -reschedule. Example: -reschedule {new date (MM/DD/YYYY)} {new time (HH:MM AM/PM)} {title}")
        return
    # separates date format into seperate values in date array
    date = content[1].split('/')
    # changes date values into int for datetime
    for x in range(len(date)):
        date[x] = int(date[x])
    # checks if valid date
    if date[0]>12 or date[0]<1 or date[1]>31 or date[1]<1 or date[2]<1000:
        await context.message.channel.send("Invalid date for -reschedule. Example: -reschedule {new date (MM/DD/YYYY)} {new time (HH:MM AM/PM)} {title}")
        return
    # separates time format into separate values in time array
    time = content[2].split(':')
    # changes time values into int for datetime
    for x in range(len(time)):
        time[x] = int(time[x])
    #adds am/pm values to time array
    time.append(content[3])
    # checks if am/pm values are correct
    if time[2].upper() != 'AM' and time[2].upper() != 'PM':
        await context.message.channel.send("Invalid time for -reschedule. Example: -schedule {new date (MM/DD/YYYY)} {new time (HH:MM AM/PM)} {title}")
        return
    # changes time into 24 hour format for datetime
    if time[2].upper() == 'PM':
        time[0]+=12
    # combines date and time into one datetime value
    eventDateTime = datetime.datetime(date[2],date[0],date[1],time[0],time[1])
    # takes the rest of content and adds it to title array
    title = []
    for x in range (4,len(content)):
        title.append(content[x])
    title = ' '.join(title)

    check = 0
    for x in range(len(client.calendar)-1):
        if client.calendar[x] == 'last':
            break
        elif client.calendar[x].get('title') == title:
            eventHold = client.calendar.pop(x)
            eventHold.update({'date': eventDateTime})
            # event insertion, sorted by date
            for i in range(len(client.calendar)):
            # if this position is empty, no date is earlier in the schedule, insert the event at this positon, leave for loop after
                if client.calendar[i] == 'last':
                    client.calendar.insert(i, eventHold) 
                    position = i
                    check = 1
                    break
                # if this position in the schedule's date is earlier than the event's, insert the event at this position, leave for loop after
                elif client.calendar[i].get('date')>eventHold.get('date'):
                    client.calendar.insert(i, eventHold)
                    position = i
                    check = 1
                    break
    if check == 1:
        await context.message.channel.send('Rescheduled event.')
    else:
        await context.message.channel.send('No event with that title found.')

@client.command()
async def poll(ctx,*,message):
    emb=discord.Embed(tile=" POLL", description=f"**Survey**: {message}")
    msg=await ctx.channel.send(embed=emb)

    await msg.add_reaction('👍')
    await msg.add_reaction('👎')
    
    
numbers = ("1️⃣","2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟")
    

@client.command(name="createpoll",aliases=["mkpoll"])
async def vote(ctx, question, *options):
    if len(options) > 10:
        await ctx.send("You can only supply a maximum of 10 options.")

    else:
        embed = discord.Embed(title = "Poll",description = f"**Survey**: {question}")

        fields = [("Options", "\n".join([f"{numbers[idx]} {option}" for idx, option in enumerate(options)]), False),("Instructions", "React to case a vote!", False)]

        for name, value, inline in fields:
            embed.add_field(name = name, value = value, inline = inline)

        message = await ctx.channel.send(embed = embed)

        for emoji in numbers[:len(options)]:
            await message.add_reaction(emoji)



# Server
# client.run(os.environ['token'])
# My test bot
client.run('ODMwNDU2NTA4MzE0ODEyNDQ2.YHG85A.nIaicdzZGjOOTAk4-P_PCYD5MEo')
# Louie
# client.run('ODA4NTEzMTYyODY4NDI0NzA0.YCHojw.g0w0z6ToLc_1tHmWFrqFqafvcR8')
