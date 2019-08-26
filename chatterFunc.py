from cowpiDB import *

#學說話
def learn(lineMessage, channelId, e_source):
    lineMes = lineMessage.replace("；",";").split(';')
    if(len(lineMes)<2):
        return "窩聽不懂啦！"
    else:
        insStatement(lineMes[1], lineMes[2:], channelId, e_source.type)
        return "好哦的喵～"

#忘記
def forget(lineMessage, channelId):
    lineMes = lineMessage.replace("；",";").split(';')
    if(len(lineMes)<2):
        return "窩聽不懂啦！"
    else:
        delStatement(lineMes[1], lineMes[2:], channelId)
        return "好哦的喵～"

#壞壞
def bad(channelId):
    last_reply_text = queryReply(channelId, 1)[0]
    adjustPrio(last_reply_text, -1)
    return  "好哦的喵～"

#回覆
def chat(lineMessage):
    return resStatement(lineMessage)

#齊推
def echo2(lineMessage, channelId):
    recent_received_texts = queryReceived(channelId, 5)
    last_reply_text = queryReply(channelId, 1)
    if recent_received_texts.count(lineMessage) < 2: return ""
    elif last_reply_text[0]==lineMessage: return ""
    else: return lineMessage
