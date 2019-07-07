from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import psycopg2
from datetime import datetime, timedelta

class LineChatBOT:
    chatbot = ChatBot(
        "LineChatBOT",
        storage_adapter = "chatterbot.storage.SQLStorageAdapter",
        database = 'postgres',
        logic_adapters=[
            {
            'import_path': 'chatterbot.logic.BestMatch',
            'statement_comparison_function': 'chatterbot.comparisons.JaccardSimilarity',
            'default_response': '可以講貓話嗎？我聽了霧撒撒！',
            'maximum_similarity_threshold': 0.1
            },
            "chatterbot.logic.MathematicalEvaluation"
        ],
        input_adapter="chatterbot.input.VariableInputTypeAdapter",
        output_adapter="chatterbot.output.OutputAdapter",
        database_uri = 'postgres://ifvbkjtshpsxqj:4972b22ed367ed7346b0107d3c3e97db14fac1dde628cd6d7f08cf502c927ee1@ec2-50-16-197-244.compute-1.amazonaws.com:5432/d6tkud0mtknjov'
    )

    def __init__(self):
        self.trainer = ChatterBotCorpusTrainer(self.chatbot)
        self.trainerList = ListTrainer(self.chatbot)
        #self.trainer.train("chatterbot.corpus.traditionalchinese")

    def getResponse(self, message=""):
        response = ""
        timeKey = ['hat time', 'now', '時間', '幾點', '時刻', '現在']
        dateKey = ['hat day', 'eekday', '天日期', '天幾號', '星期幾', '幾月幾']
        weekDay = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
        dt = datetime.now() + timedelta(hours = 8)
        if any(s in message for s in timeKey):
            response = "現在時間 (UTC+8)：" + str(dt.hour) + ":" + str(dt.minute)
        elif  any(s in message for s in dateKey) or any(s == message for s in ["前天", "昨天", "今天", "明天", "後天"]):
            tmp = "今"
            if "明天" in message:
                dt += timedelta(days = 1)
                tmp = "明"
            elif "昨天" in message:
                dt -= timedelta(days = 1)
                tmp = "昨"
            elif "後天" in message:
                dt += timedelta(days = 2)
                tmp = "後"
            elif "前天" in message:
                dt -= timedelta(days = 2)
                tmp = "前"
            response = tmp + "天是 " + str(dt.year) + "年" + str(dt.month) + "月" + str(dt.day) + "日 " + weekDay[dt.weekday()]
        else:
            response = self.chatbot.get_response(message)
        return response