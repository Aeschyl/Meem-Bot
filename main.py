# dependencies
import discord
import random
import asyncio
import json
import os
from commands import reddit, weather, ranking

client = discord.Client()

# variables
prefix = "~"


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author != client.user:

        with open('users.json', 'r') as f:
            users = json.load(f)

        await ranking.update_data(users, message.author, 5)
        await ranking.level_up(users, message.author, message.channel)

        with open('users.json', 'w') as f:
            json.dump(users, f)

        if message.content.startswith(prefix):

            # hi/hello - yello
            if f"{prefix}hi" == str.strip(message.content.lower()) or f"{prefix}hello" == str.strip(
                    message.content.lower()):

                greeting_list = ["yello!", "hello!", "hi there!", "hi!"]

                await message.channel.send(random.choice(greeting_list))

            # bye
            elif f"{prefix}bye" == str.strip(message.content.lower()):
                await message.channel.send("Ok, then get out of here")

            # no u
            elif message.content.startswith(f"{prefix}suck"):
                await message.channel.send("no u")

            # gives the weather of the city mentioned
            elif message.content.startswith(f"{prefix}weather"):
                await weather.weather(message)

            # clears the channel
            elif message.content.startswith(f"{prefix}clear"):
                if message.author.guild_permissions.administrator:
                    global clear_user
                    clear_user = message.author
                    global clear_all
                    global clear_message
                    clear_message = message
                    if f"{prefix}clear" == str.strip(message.content.lower()):
                        confirmation_msg = await message.channel.send("Are you sure?")
                        await confirmation_msg.add_reaction('✅')
                        await confirmation_msg.add_reaction('❌')
                        await message.channel.send("React with one of the options!")
                        clear_all = True

                    elif int(message.content[7:]) in range(0, 10000):
                        confirmation_msg = await message.channel.send("Are you sure?")
                        await confirmation_msg.add_reaction('✅')
                        await confirmation_msg.add_reaction('❌')
                        await message.channel.send("React with one of the options!")
                        clear_all = False

                    elif int(message.content[7:]) >= 10000:
                        await message.channel.send(
                            "Sorry, but you inputted too big a number to delete. Start smaller than 10000")
                    elif int(message.content[7:]) == 0:
                        await message.channel.send("WHY WOULD YOU WANT TO DELETE ZERO MESSAGES? IDIOT")
                    elif int(message.content[7:]) < 0:
                        await message.channel.send("You can't delete negative messages, you cretin")
                else:
                    await message.channel.send("Sorry pleb, command reserved for people better than you.")

            # memes
            elif f"{prefix}meme" == str.strip(message.content.lower()) or f"{prefix}memes" == str.strip(
                    message.content.lower()):

                list_for_meme_or_memes = [1, 2]

                meme_or_memes_choice = random.choice(list_for_meme_or_memes)

                if meme_or_memes_choice == 1:
                    await reddit.subreddit_result("memes", message)

                elif meme_or_memes_choice == 2:
                    await reddit.subreddit_result("meme", message)

                else:
                    await message.channel.send("I'm sorry, I was unable to get the results. Please try again later.")

            # holup
            elif f"{prefix}holup" == str.strip(message.content.lower()):
                await reddit.subreddit_result("holup", message)

            # clever comebacks
            elif f"{prefix}cc" == str.strip(message.content.lower()) or f"{prefix}clevercomebacks" == str.strip(
                    message.content.lower()):
                await reddit.subreddit_result("clevercomebacks", message)

            # cringe
            elif f"{prefix}cringe" == str.strip(message.content.lower()) or f"{prefix}cringepics" == str.strip(
                    message.content.lower()):
                await reddit.subreddit_result("cringepics", message)

            elif str.strip(message.content.lower()) in [f'{prefix}rank', f'{prefix}level', f'{prefix}experience',
                                                        f'{prefix}xp', f'{prefix}exp']:
                await ranking.show_rank(users, message.author, message)

            else:  # this is for when the sender uses an ! but does not follow up with a viable command
                await message.channel.send("Sorry, I do not understand that")

        else:  # this is for when the sender does not use a exclamation mark (!)
            return

    else:  # this is for when the bot is the sender, so an empty return because it is not supposed to respond to itself.
        return


@client.event
async def on_reaction_add(reaction, user):
    if "Are you sure?" == reaction.message.content:
        if reaction.count == 2 and clear_user == user:
            if reaction.emoji == '✅':
                if clear_all:
                    await clear_message.channel.send("Deleting all messages:")
                    await asyncio.sleep(0.75)
                    await clear_message.channel.purge(limit=10001)
                elif not clear_all:
                    if int(clear_message.content[7:]) == 1:
                        input_limit = int(clear_message.content[7:]) + 4
                        await clear_message.channel.send(f"Deleting {clear_message.content[7:]} message:")
                        await asyncio.sleep(0.75)
                        await clear_message.channel.purge(limit=input_limit)
                    else:
                        input_limit = int(clear_message.content[7:]) + 4
                        await clear_message.channel.send(f"Deleting {clear_message.content[7:]} messages:")
                        await asyncio.sleep(0.75)
                        await clear_message.channel.purge(limit=input_limit)
            elif reaction.emoji == '❌':
                await clear_message.channel.send("Message clearing canceled")
                await asyncio.sleep(0.75)
                await clear_message.channel.purge(limit=4)

discord_key = ''

client.run(discord_key)
