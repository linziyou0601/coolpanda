from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

class LineChatBOT:
    # 建立一個 ChatBot
    chatbot = ChatBot(
        # 這個 ChatBot 的名字叫做 LineChatBOT
        "LineChatBOT",
        storage_adapter = "chatterbot.storage.JsonFileStorageAdapter",
        # 設定訓練的資料庫輸出於根目錄，並命名為 LineChatBOT_DB.json
        database = "./LineChatBOT_DB.json"
    )

    def __init__(self):
        self.chatbot.set_trainer(ChatterBotCorpusTrainer)
        # 基於英文的自動學習套件
        #self.chatbot.train("chatterbot.corpus.english")
        # 載入(簡體)中文的基本語言庫
        self.chatbot.train("chatterbot.corpus.chinese")
        # 載入(簡體)中文的問候語言庫
        #self.chatbot.train("chatterbot.corpus.chinese.greetings")
        # 載入(簡體)中文的對話語言庫
        #self.chatbot.train("chatterbot.corpus.chinese.conversations")

    def getResponse(self, message=""):
        return self.chatbot.get_response(message)