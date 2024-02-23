# bot.py
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

def create_chatbot():
    chatbot = ChatBot('MyBot')
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train('chatterbot.corpus.english')
    return chatbot

def get_chatbot_response(chatbot, user_input):
    response = chatbot.get_response(user_input)
    return str(response)
