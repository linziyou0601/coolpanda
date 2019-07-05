from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import *
import psycopg2

class LineChatBOT:
    chatbot = ChatBot(
        "LineChatBOT",
        storage_adapter = "chatterbot.storage.SQLStorageAdapter",
        database = 'postgres',
        logic_adapters=[
            {
                "import_path": "chatterbot.logic.BestMatch",
                "statement_comparison_function": levenshtein_distance,
                "response_selection_method": get_first_response
            },
            "chatterbot.logic.MathematicalEvaluation"
        ],
        input_adapter="chatterbot.input.VariableInputTypeAdapter",
        output_adapter="chatterbot.output.OutputAdapter",
        database_uri = 'postgres://ifvbkjtshpsxqj:4972b22ed367ed7346b0107d3c3e97db14fac1dde628cd6d7f08cf502c927ee1@ec2-50-16-197-244.compute-1.amazonaws.com:5432/d6tkud0mtknjov'
    )

    def __init__(self):
        trainer = ChatterBotCorpusTrainer(self.chatbot)
        #trainer.train("chatterbot.corpus.traditionalchinese")

    def getResponse(self, message=""):
        timeKey = ['What time', 'what time', 'now', '時間', '幾點', '時刻']
        response = "現在時間" if any(s in message for s in timeKey) else self.chatbot.get_response(message)
        return response