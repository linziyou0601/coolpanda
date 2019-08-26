from cowpiDB import *

####主聊天功能
##自動學習
def autolearn(my, lineMessage, channelId, e_source):
    insStatement(my, [lineMessage], channelId, e_source.type)
##學說話
def learn(lineMessage, channelId, e_source):
    lineMes = [x for x in lineMessage.replace("；",";").split(';') if x != ""]
    #若語法正確才加入詞條
    if(len(lineMes)<3):
        return "窩聽不懂啦！"
    else:
        insStatement(lineMes[1], lineMes[2:], channelId, e_source.type)
        return "好哦的喵～"
##忘記
def forget(lineMessage, channelId):
    lineMes = [x for x in lineMessage.replace("；",";").split(';') if x != ""]
    #若語法正確才刪除詞條
    if(len(lineMes)<3):
        return "窩聽不懂啦！"
    else:
        delStatement(lineMes[1], lineMes[2:], channelId)
        return "好哦的喵～"
##壞壞
def bad(channelId):
    #批次降低資料庫內本次回話的關鍵字權重
    adjustPrio(queryReceived(channelId, 1)[0], queryReply(channelId, 1)[0], -1)
    return "好哦的喵～"
##回覆(隨機回覆)
def chat(lineMessage, channelId):
    rand = 1 if lineMessage[0:3]=='牛批貓' or lineMessage[0:2]=='抽籤' else 0
    return resStatement(lineMessage[3:] if rand else lineMessage, channelId, rand)
##成功回話時增加權重
def validReply(lineMessage, reply, channelId):
    adjustPrio(lineMessage, reply, 1, "" if queryUser(channelId)[1] else channelId)
##齊推
def echo2(lineMessage, channelId):
    if queryReceived(channelId, 5).count(lineMessage) < 2: return ""
    elif queryReply(channelId, 1)[0]==lineMessage: return ""
    else: return lineMessage

####功能開關
def globaltalk(lineMessage, channelId):
    if "可以說別人教的話" in lineMessage: editChannelGlobalTalk(channelId, 1)
    elif any(s in lineMessage for s in ["不可以說別人教的話", "不能說別人教的話"]): editChannelGlobalTalk(channelId, 0)
    return "好哦的喵～"
def mute(lineMessage, channelId):
    if any(s in lineMessage for s in ["牛批貓說話", "牛批貓講話"]): editChannelMute(channelId, 0)
    elif any(s in lineMessage for s in ["牛批貓安靜", "牛批貓閉嘴"]): editChannelMute(channelId, 1)
    return "好哦的喵～"
def currentStatus(channelId):
    status = queryUser(channelId)
    return "說話模式："+("" if status[1] else "不")+"可以說別人教的話\n"+"說話狀態："+("安靜" if status[2] else "可以說話")
