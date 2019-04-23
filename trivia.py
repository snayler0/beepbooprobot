import random
import os
import yaml

class Trivia:

    def __init__(self):
        self.running = False
        self.topic = None
        self.current_question = None
        self.score = {}
        self.datadir = "triviadata"
        self.channel = None
        self.asked_questions = []

    def start(self, channel, topic):
        if not os.path.exists('{0}/{1}'.format(self.datadir,topic)):
            return 'The trivia topic: "{0}" does not exist yet. To create it, use !trivia create {0}'.format(topic)
        else:
            self.topic = topic
            self.channel = channel
            return 'Starting a trivia game in the "{0}" channel based on the "{1}" topic'.format(channel, topic)
    
    def create(self, topic):
        if not os.path.exists('{0}/{1}'.format(self.datadir,topic)):
            f = open('{0}/{1}'.format(self.datadir,topic), 'w+')
            data = {'questions'}
            yaml.dump(data, f)
            f.close()
            print(data)
            return """
The trivia topic: "{0}" has been created!

    To add a question to it, use !trivia add_question {0}
""".format(topic)
        else:
            return """
The trivia topic: "{0}" already exists!

    To edit it, use !trivia edit {0}
    To add a question to it, use !trivia add_question {0}
""".format(topic)

    def help(self):
        return """
It looks like you need help! Let me do my best clippy impression. Actually nah, here\'s a list of commands and how to use them instead:

    help                - Returns the message that you are already reading right now... :)
    start TOPIC         - Tries to start a new trivia game based on the provided TOPIC in your current channel
    create TOPIC        - Starts an interactive process to add a new trivia topic based on the provided TOPIC. (requires the @triviamod role)
    edit TOPIC          - Starts an interactive process to edit the provided TOPIC. (requires the @triviamod role)
    add_question TOPIC  - Starts an interactive process to add a question to the provided TOPIC. (requires the @triviamod role)

"""