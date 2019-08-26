from cowpiDB import *

#學說話
def learn(lineMessage, channelId, e_source):
    lineMes = [x for x in lineMessage.replace("；",";").split(';') if x != ""]
    if(len(lineMes)<3):
        return "窩聽不懂啦！"
    else:
        insStatement(lineMes[1], lineMes[2:], channelId, e_source.type)
        return "好哦的喵～"

#忘記
def forget(lineMessage, channelId):
    lineMes = [x for x in lineMessage.replace("；",";").split(';') if x != ""]
    if(len(lineMes)<3):
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
def chat(lineMessage, channelId):
    return resStatement(lineMessage, channelId)

#齊推
def echo2(lineMessage, channelId):
    recent_received_texts = queryReceived(channelId, 5)
    last_reply_text = queryReply(channelId, 1)
    if recent_received_texts.count(lineMessage) < 2: return ""
    elif last_reply_text[0]==lineMessage: return ""
    else: return lineMessage

#功能開關
def globaltalk(lineMessage, channelId):
    if "可以說別人教的話" in lineMessage: editChannelGlobalTalk(channelId, 1)
    elif any(s in lineMessage for s in ["不可以說別人教的話", "不能說別人教的話"]): editChannelGlobalTalk(channelId, 0)
def mute(lineMessage, channelId):
    if "牛批貓說話" in lineMessage: editChannelMute(channelId, 1)
    elif any(s in lineMessage for s in ["牛批貓安靜", "牛批貓閉嘴"]): editChannelMute(channelId, 0)
def currentStatus(channelId):
    status = queryUser(channelId);
    return "說話模式："+("" if status[1] else "不")+"可以說別人教的話/n"+"說話狀態："+("可以說話" if status[2] else "安靜")
