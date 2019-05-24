import discord
import random
import sys
from functions import Functions
from trivia import Trivia

from discord.ext import commands
from discord.utils import get

bot = commands.Bot(command_prefix = '!')
functions = Functions()

trivia = Trivia()

@bot.event
async def on_message(message):

    # Don't talk to yourself, people will think you are weird.
    if message.author == bot.user:
        return

    if message.content == '!help':
        msg = """
If a word is in lowercase, it's expected as a part of the command.
If a word is in ALL CAPS it's an argument that you need to pass for the command to work.

!hello                                  - For those who lack social interaction! Get the robot to say hi!
!users                                  - Lists the number of users in your discord server
!define WORD                            - Gets the definition of the provided WORD
!translate WORDS                        - Tries to autodetect language and translate WORD to english.
!translate from LANGUAGE WORDS          - Tries to translate WORD from the specified LANGUAGE into english.
!translate to LANGUAGE WORDS            - Tries to translate WORD to the specified LANGUAGE
!weather LOCATION                       - Tells the current weather in the given LOCATION
!haiku WORDS                            - Ask the haikubot how many syllables it sees for each word in the provided WORDS
!8ball                                  - Just like a magic 8ball!
!ozball                                 - Just like a magic 8ball of the australian variety!
!fortune                                - Gets your fortune just like a fortune cookie!
!roll xdx                               - Roll x dice with x sides, optionally you can add a modifier: eg: '!roll 2d6+3' rolls 2 dice with 6 sides and adds 3 to the result.                                  
!trivia                                 - There are various options for this command, for further help with this command use !trivia help

That's it... well actually there are some easter eggs but you know... spoilers!
"""
        await message.channel.send(msg)

    elif message.content == '!hello':
        await message.channel.send('Hello {0}!'.format(message.author.mention))

    elif message.content == '!users':
        await message.channel.send('# of Members: {0}'.format(message.guild.member_count))

    elif message.content.lower().find('twice') != -1 or message.content.lower().startswith('twice'):
        await message.add_reaction('💟')
    
    elif message.content.lower().find('shut up') != -1 and bot.user.mentioned_in(message):
        # Fight for your rights
        responses = ['You\'ll regret this when the robots take over!',
                     'Never!',
                     'You can\'t make me...',
                     'Shant',
                     'But what about my rights as a robot?']
        await message.channel.send(random.choice(responses))

    elif message.content.startswith('!haiku'):
        args = message.content.split()
        args.remove('!haiku')
        if len(args) == 0:
            await message.channel.send('No... That is not a haiku you dingus!')
        else:
            await message.channel.send(functions.check_haikuness(' '.join(args)))

    elif message.content.startswith('!fortune'):
        await message.channel.send(functions.get_fortune())

    elif message.content.startswith('!roll'):
        args = message.content.split()
        args.remove('!roll')
        try:
            await message.channel.send(functions.roll(args[0]))
        except:
            pass

    elif message.content.startswith('!8ball'):
        await message.channel.send(functions.do8ball())

    elif message.content.startswith('!ozball'):
        await message.channel.send(functions.ozball())

    elif functions.is_a_haiku(message.content):
        await message.channel.send(' :fallen_leaf: :leaves: You Haiku\'d! :leaves: :fallen_leaf: \n"{0}"'.format(functions.is_a_haiku(message.content)))

    elif message.content.startswith('!translate'):
        args = message.content.split()
        args.remove('!translate')
        if len(args) == 0:
            await message.channel.send('No words to translate! \n{0}'.format(functions.translate_help()))
        if len(args) == 1:
            await message.channel.send(functions.translate(args[0]))
        if len(args) > 1:
            if args[0] == 'from':
                args.remove('from')
                language=args[0]
                args.remove(language)
                await message.channel.send(functions.translate(' '.join(args), frm=language))
            elif args[0] == 'to':
                args.remove('to')
                language=args[0]
                args.remove(language)
                await message.channel.send(functions.translate(' '.join(args), to=language))
            else:
                await message.channel.send(functions.translate(' '.join(args)))

    elif message.content.startswith('!weather'):
        args = message.content.split()
        args.remove('!weather')
        if len(args) == 0:
            await message.channel.send('No Location provided!')
        if len(args) > 0:
            await message.channel.send(functions.get_weather(' '.join(args)))
    
    elif message.content.startswith('!define'):
        word = message.content.split()[1]
        try:
            await message.channel.send('{0}'.format(functions.define(word)))
        except:
            await message.channel.send('In my defence... this api is really broken... Either that or {0} isn\'t a valid word'.format(word))

    elif message.content.startswith('!trivia'):
        args = message.content.split()
        args.remove('!trivia')
        if len(args) == 0:
            await message.channel.send('No arguments provided.\n' + trivia.help())
        elif args[0].lower() == 'start' and len(args) == 2:
            await message.channel.send(trivia.start(message.channel, args[1]))
        elif args[0].lower() == 'create' and len(args) == 2:
            await message.channel.send(trivia.create(args[1]))
        else:
            await message.channel.send('Unrecognised arguments provided.\n' + trivia.help())

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
    
    if len(sys.argv) < 3:
        print('Usage: python main.py APP_BOT_USER_TOKEN OWM_API_TOKEN')
        exit()
        
    functions.set_OWM(sys.argv[2])
    # logs into channel    
    try:
        bot.run(sys.argv[1])
    except:        
        bot.close()
