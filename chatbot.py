from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import psycopg2

class LineChatBOT:
    chatbot = ChatBot(
        "LineChatBOT",
        storage_adapter = "chatterbot.storage.SQLStorageAdapter",
        database = 'd6tkud0mtknjov',
        database_uri = 'postgres://ifvbkjtshpsxqj:4972b22ed367ed7346b0107d3c3e97db14fac1dde628cd6d7f08cf502c927ee1@ec2-50-16-197-244.compute-1.amazonaws.com:5432/d6tkud0mtknjov'
    )

    def __init__(self):
        trainer = ChatterBotCorpusTrainer(self.chatbot)
        trainer.train("chatterbot.corpus.traditionalchinese.food")

    def getResponse(self, message=""):
        response = self.chatbot.get_response(message)
        return response