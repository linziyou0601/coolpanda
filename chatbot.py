from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import psycopg2

class LineChatBOT:
    chatbot = ChatBot(
        "LineChatBOT",
        storage_adapter = "chatterbot.storage.SQLStorageAdapter",
        database = 'postgres',
        database_uri = 'postgres://postgres:Mm552288369@localhost:5432/postgres'
    )

    def __init__(self):
        trainer = ChatterBotCorpusTrainer(self.chatbot)
        trainer.train("chatterbot.corpus.traditionalchinese")

    def getResponse(self, message=""):
        response = self.chatbot.get_response(message)
        return response