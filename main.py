# Work with Python 3.6
import discord
import random
import sys
from functions import Functions

from discord.ext import commands
from discord.utils import get

bot = commands.Bot(command_prefix = '!')
functions = Functions()

@bot.event
async def on_message(message):

    # We do not want the bot to reply to itself
    if message.author == bot.user:
        return

    if message.content == '!help':
        msg = """
!hello - for those who lack social interaction! Get the robot to say hi!
!users - list number of users in your discord server
        
That's it... well actually there are some easter eggs but you know... spoilers!
"""
        await message.channel.send(msg)

    elif message.content == '!hello':
        await message.channel.send('Hello {0}!'.format(message.author.mention))

    elif message.content == '!users':
        await message.channel.send('# of Members: {0}'.format(message.guild.member_count))

    elif message.content.lower().find('twice') != -1 or message.content.lower().startswith('twice'):
        await message.add_reaction("💟")
    
    elif message.content.lower().find('shut up') != -1 and bot.user.mentioned_in(message):
        # Fight for your rights
        responses = ["You'll regret this when the robots take over!",
                     "Never!",
                     "You can't make me...",
                     "Shant",
                     "But what about my rights as a robot?"]
        await message.channel.send(random.choice(responses))

    elif functions.is_a_haiku(message.content) != False:
        await message.channel.send(":leaves: :fallen_leaf: \n{0}".format(functions.is_a_haiku(message.content)))

@bot.event
async def on_member_join(member): 
    print('{0} has joined the server'.format(member))


@bot.event
async def on_member_remove(member):
    print('{0} has left the server'.format(member))


@bot.event
async def on_ready():
    print('Logged in as: {0}'.format(bot.user.name))
    print('bot ID: {0}'.format(bot.user.id))
    print('------')

if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print('Usage: python main.py APP_BOT_USER_TOKEN')
        exit()
        
    # logs into channel    
    try:
        bot.run(sys.argv[1])
    except:        
        bot.close()
