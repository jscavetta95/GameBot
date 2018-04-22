import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random

bot = commands.Bot(command_prefix='#')

GAME_LIST = "game_list.txt"

@bot.event
async def on_ready():
    print ("Ready.")

@bot.command(pass_context=True)
async def game_list(ctx, *games):
    await bot.say("Updating game list...")
    game_list = ""
    with open(GAME_LIST, "w") as output_handle:
        for game in games:
            if(game != ""):
                output_handle.write(game + "\n")
                game_list += ("\t" + game + "\n")
    await bot.say("Game List:\n" + game_list)

@bot.command(pass_context=True)
async def vote(ctx, num_voters):
    games = ""
    with open(GAME_LIST, "r") as output_handle:
        games = output_handle.read()
    games = games.split("\n")
    weighted_choices = list()
    for game in games:
        if(game != ""):
            print("GAME: " + game)
            await bot.say("Vote on {}! (0-5)".format(game))
            def check(msg):
                try:
                    return int(msg.content) in range(6)
                except :
                    return False
            total_vote = 0
            for i in range(int(num_voters)):
                msg = await bot.wait_for_message(check=check)
                total_vote += int(msg.content)
            for i in range(total_vote):
                weighted_choices.append(game)
        else:
            games.remove(game)
    choices = random.sample(weighted_choices, 1)
    await bot.say("Play:")
    for choice in choices:
        await bot.say("\t" + choice)

bot.run("NDM3NDUxNzAwNjk4MDg3NDI1.Db2SVA.7M7UxEy9F9-SN5IrtTTOFg7v-mQ")