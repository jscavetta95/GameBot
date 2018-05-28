"""GameBot
Author: Joseph Scavetta
Last Update: 5/28/2018

Creates and maintains a list of games that users can vote on.
Games to play are listed based on a weighted randomization.
"""

import asyncio
import random
import discord
from discord.ext import commands
from discord.ext.commands import Bot

BOT = commands.Bot(command_prefix='#')

GAME_LIST = "game_list.txt"

def __game_list__():
    """Reads and returns the game list."""
    with open(GAME_LIST, "r") as output_handle:
        games = output_handle.read()
    return games

@BOT.event
async def on_ready():
    """Readies the bot."""
    print("Ready.")

@BOT.command(pass_context=True)
async def games(ctx):
    """Bot command to list the games currently in the list."""
    await BOT.say("Game List:\n" + __game_list__())

@BOT.command(pass_context=True)
async def add_game(ctx, game_to_add):
    """Bot command to add a game to the list."""
    with open(GAME_LIST, 'r') as output_handle:
        games = output_handle.read()
    games = games.split("\n")
    games = list(filter(None, games))
    games.append(game_to_add)
    with open(GAME_LIST, 'w') as output_handle:
        for game in games:
            output_handle.write(game + "\n")
    await BOT.say("Game List:\n" + __game_list__())

@BOT.command(pass_context=True)
async def remove_game(ctx, game_to_remove):
    """Bot command to remove a game from the list."""
    with open(GAME_LIST, 'r') as output_handle:
        games = output_handle.read()
    games = games.split("\n")
    if game_to_remove in games:
        games.remove(game_to_remove)
        with open(GAME_LIST, 'w') as output_handle:
            for game in games:
                output_handle.write(game + "\n")
        await BOT.say("Game List:\n" + __game_list__())
    else:
        await BOT.say("Game not found :^)")

@BOT.command(pass_context=True)
async def update_games(ctx, *games):
    """Bot command to update the entire game list."""
    with open(GAME_LIST, "w") as output_handle:
        for game in games:
            if game != "":
                output_handle.write(game + "\n")
    await BOT.say("Game List:\n" + __game_list__())

@BOT.command(pass_context=True)
async def vote(ctx, num_voters):
    """Bot command start the game to play vote."""
    games = ""
    with open(GAME_LIST, "r") as output_handle:
        games = output_handle.read()
    games = games.split("\n")
    weighted_choices = list()

    for game in games:
        if game != "":
            await BOT.say("Vote on {}! (0-5)".format(game))

            def check(msg):
                """True if the message contains a number from 0 to 5."""
                try:
                    return int(msg.content) in range(6)
                except:
                    return False

            total_vote = 0
            skip = False
            for i in range(int(num_voters)):
                msg = await BOT.wait_for_message(check=check)
                msg = int(msg.content)

                if msg == 0:
                    skip = True
                else:
                    total_vote += msg

            if not skip:
                for i in range(total_vote):
                    weighted_choices.append(game)
        else:
            games.remove(game)

    choices = list()
    while weighted_choices:
        choice = random.sample(weighted_choices, 1)[0]
        weighted_choices[:] = (value for value in weighted_choices if value != choice)
        choices.append(choice)

    message = "Play:\n"
    i = 1
    for choice in choices:
        message = ("{}\t{}. {}\n".format(message, i, choice))
        i += 1
    await BOT.say(message)

BOT.run("NDM3NDUxNzAwNjk4MDg3NDI1.Db2SVA.7M7UxEy9F9-SN5IrtTTOFg7v-mQ")
