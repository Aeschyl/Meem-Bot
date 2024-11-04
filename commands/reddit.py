#memes and others from reddit

import discord
import praw
import random

async def subreddit_result(sub, message):
    reddit = praw.Reddit(client_id="fP0Q4SjPGJYNHQ", client_secret="IxnUxm4Jj_fTmVkGnIMtr0L9ckqYRw",
                         username="discord_bot_py", password="REDACTED", user_agent="meem_bot", check_for_async=False) #The password is you-know-what but without punctuation
    all_submissions = []

    subreddit = reddit.subreddit(sub)

    top = subreddit.top(limit=30, time_filter="day")

    for submission in top:
        all_submissions.append(submission)

    random_sub = random.choice(all_submissions)

    title = random_sub.title
    url = random_sub.url

    em = discord.Embed(title=title)

    em.set_image(url=url)

    await message.channel.send(embed=em)
