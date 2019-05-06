import syllables
from PyDictionary import PyDictionary
from googletrans import Translator
import pyowm
import json
import inflect
import string
import random
import ast

class Functions:
    
    def __init__(self):
        self.dictionary = PyDictionary()
        self.translator = Translator()
        self.owm = None
        self.p = inflect.engine()
        self.debug = False
        self.binary_ops = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod)

    def set_OWM(self, owm_token):
        self.owm = pyowm.OWM(owm_token) 

    def define(self, word):
        try:
            definition = self.dictionary.meaning(word)
            response = ''
            counter = 1
            for wordtype in definition:
                for answer in definition[wordtype]:
                    response += '{0}. ({1}): {2}\n'.format(counter, wordtype, answer)
                    counter += 1
            return response
        except:
            return 'In my defence... this api is really broken... Either that or {0} isn\'t a valid word'.format(word)

    def get_weather(self, location):
    # try:
        observation = self.owm.weather_at_place(location)
        weather = observation.get_weather()

        clouds = weather.get_clouds()
        rain = weather.get_rain()
        snow = weather.get_snow()
        wind = weather.get_wind()
        humidity = weather.get_humidity()
        celsius = weather.get_temperature(unit='celsius')
        fahrenheit = weather.get_temperature('fahrenheit')
        status = weather.get_detailed_status()

        rain_info = None
        if '3h' in rain:
            rain_info = '{0}mm in the last 3 hours'.format(rain['3h'])
        elif '1h' in rain:
            rain_info = '{0}mm in the last 1 hour'.format(rain['1h'])
        else:
            rain_info = 'No data recently recorded.'

        snow_info = None
        if '3h' in snow:
            snow_info = '{0}mm in the last 3 hours'.format(snow['3h'])
        elif '1h' in snow:
            snow_info = '{0}mm in the last 1 hour'.format(snow['1h'])
        else:
            snow_info = 'No data recently recorded.'

        return """
The weather in {0} is {1}.
CURRENT :thermometer:: {2}°C ({5}°F)
MIN :thermometer: {3}°C ({6}°F)
MAX :thermometer: {4}°C ({7}°F)
humidity :sweat_drops:: {8}% 
clouds :cloud:: {9}%
rain :cloud_rain:: {10}
snow :snowflake:: {11}
wind :dash:: {12} meters/second
""".format(location, status, celsius['temp'], celsius['temp_min'], celsius['temp_max'], fahrenheit['temp'], fahrenheit['temp_min'], fahrenheit['temp_max'],
humidity, clouds, rain_info, snow_info, wind['speed'])
    # except:
    #     return 'Failed to get weather for {0}'.format(location)

    def format_translation(self, translation):
        response = """
Translated: {0}
From: {1}
To: {2}
Translation: {3}
""".format(translation.origin, translation.src, translation.dest, translation.text)
        if translation.pronunciation:
            response += 'Pronunciation: {0}'.format(translation.pronunciation) 

        return response
    
    def translate(self, words, to=None, frm=None):
        if to:
            translation = self.translator.translate(words, dest=to)
        elif frm:
            translation = self.translator.translate(words, src=frm)
        else:
            translation = self.translator.translate(words)

        return self.format_translation(translation)

    def translate_help(self):
        return """
!translate WORD                 - Tries to autodetect language and translate WORD to english.
!translate from LANGUAGE WORD   - Tries to translate WORD from the specified LANGUAGE into english.
!translate to LANGUAGE WORD     - Tries to translate WORD to the specified LANGUAGE
"""

    def roll(self, incoming):
        options = incoming.split('d')
        if len(options) == 2:
            numdice = options[0]
            diceface=options[1]
            if '+' in options[1]:
                diceface = options[1].split('+')[0]
                modifier = '+{0}'.format(options[1].split('+')[1])
            elif '-' in options[1]:
                diceface = options[1].split('-')[0]
                modifier = '-{0}'.format(options[1].split('-')[1])
            elif '/' in options[1]:
                diceface = options[1].split('/')[0]
                modifier = '/{0}'.format(options[1].split('/')[1])
            elif '*' in options[1]:
                diceface = options[1].split('*')[0]
                modifier = '*{0}'.format(options[1].split('*')[1])
            else:
                modifier = '+0'
            possible_total=int(numdice) * int(diceface)
            roll = '{0}{1}'.format(random.randint(1, possible_total), modifier)
            result = eval(roll)
            return result
        else:
            return 'I can\'t roll {0}!'.format(incoming)

    def do8ball(self):
        options = ["It is certain.",
                   "It is decidedly so.",
                   "Without a doubt.",
                   "Yes - definitely.",
                   "You may rely on it.",
                   "As I see it, yes.",
                   "Most likely.",
                   "Outlook good.",
                   "Yes.",
                   "Signs point to yes.",
                   "Reply hazy, try again.",
                   "Ask again later.",
                   "Better not tell you now.",
                   "Cannot predict now.",
                   "Concentrate and ask again.",
                   "Don't count on it.",
                   "My reply is no.",
                   "My sources say no.",
                   "Outlook not so good.",
                   "Very doubtful."]

        return random.choice(options)

    def ozball(self):
        options = ["Bloody Oath!",
                   "Deadset, mate.",
                   "Without a doubt.",
                   "Nah, yeah.",
                   "Strewth!",
                   "No worries, mate, she'll be right.",
                   "Better than a kick up the backside.",
                   "Piece of Piss",
                   "Right as rain",
                   "She'll be apples",
                   "Six of one, half a dozen of the other",
                   "Buggered if i know",
                   "I'm on the blink.",
                   "It's a fish outta water.",
                   "Give it another bash ya drongo.",
                   "Yeah, nah",
                   "Tell him he's dreamin'.",
                   "Buckley's.",
                   "You're off ya rocker!",
                   "You've gotta be joking."]

        return random.choice(options)

    def check_haikuness(self, incoming):
        exclude = set(string.punctuation)
        incoming = ''.join(ch for ch in incoming if ch not in exclude)
        words = str(incoming).split()
        with open('haiku_overrides.json', 'r') as f:
            overrides = json.load(f)
        
        response = ''
        for word in words:
            if word in overrides:
                response += '{0}({1}) '.format(word, overrides[word])
            else:
                response += '{0}({1}) '.format(word, syllables.estimate(word))

        return response

    def is_a_haiku(self, incoming):
        if self.debug:
            print('----------CHECKING FOR HAIKU----------')
        haiku = False
        exclude = set(string.punctuation)
        incoming = ''.join(ch for ch in incoming if ch not in exclude)
        words = str(incoming).split()
        with open('haiku_overrides.json', 'r') as f:
            overrides = json.load(f)

        syl_count = 0
        for word in words:
            if word in overrides:
                syl_count += overrides[word]
                if self.debug:
                    print('{0} ({1}). Total: {2}'.format(word, overrides[word], syl_count))
            else:
                try:
                    word = self.p.number_to_words(int(word))
                except ValueError:
                    pass
                finally:
                    syl_count += syllables.estimate(word)
                    if self.debug:
                        print('{0} ({1}). Total: {2}'.format(word, syllables.estimate(word), syl_count))

        if syl_count == 17:
            line = ""
            lines = []
            syl_count = 0

            for word in words:
                try:
                    word = self.p.number_to_words(int(word))
                except ValueError:
                    pass
                finally:
                    word = word.lower()

                if len(lines) == 3 and syllables.estimate(word) > 0:
                    if self.debug:
                        print(lines)
                        print('leftover word: {0} with {1} syllables'.format(word, syllables.estimate(word)))
                    haiku = False
                    break

                if len(lines) == 2:
                    if syl_count < 5:
                        if word in overrides:
                            syl_count += overrides[word]
                        else:
                            syl_count += syllables.estimate(word)
                        line = line + word + " "
                    
                    if syl_count == 5:
                        if self.debug:
                            print('Line 3 complete with {0} sylables: {1}'.format(syl_count, line))
                        lines.append(line.strip())
                        haiku = True
                        line = ""
                        syl_count = 0
                    elif syl_count > 5:
                        haiku = False
                        break

                if len(lines) == 1:
                    if syl_count < 7:
                        if word in overrides:
                            syl_count += overrides[word]
                        else:
                            syl_count += syllables.estimate(word)
                        line = line + word + " "
                    
                    if syl_count == 7:
                        if self.debug:
                            print('Line 2 complete with {0} sylables: {1}'.format(syl_count, line))
                        lines.append(line.strip())
                        line = ""
                        syl_count = 0
                    elif syl_count > 7:
                        haiku = False
                        break

                if len(lines) == 0:
                    if syl_count < 5:
                        if word in overrides:
                            syl_count += overrides[word]
                        else:
                            syl_count += syllables.estimate(word)
                        line = line + word + " "
                    
                    if syl_count == 5:
                        if self.debug:
                            print('Line 1 complete with {0} sylables: {1}'.format(syl_count, line))
                        lines.append(line.strip())
                        line = ""
                        syl_count = 0
                    elif syl_count > 5:
                        haiku = False
                        break
        else:
            pass

        if haiku:
            if self.debug:
                print('----------HAIKU----------')
            return "\n".join(lines)
        else:
            if self.debug:
                print('----------NOT A HAIKU----------')
            return False

# def main():
#     message = input('gimmie a Haiku: ')
#     funct = Functions()
#     funct.is_a_haiku(message)

# if __name__ == "__main__":
#     main()