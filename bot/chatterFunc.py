##########聊天機器人，聊天功能、關鍵字資料呼叫##########
from .cowpiDB import *
from .crawlerFunc import *
from datetime import datetime, timedelta
import pytz, re, random

####關鍵字功能
def AQI(site):
    return getAQI(site)
def Weather(site):
    PATTERN = '((明|後|大後)[早晚天]|[一下]週|[早晚]上|中午|凌晨|未來)'
    return [getWeather(site, True), 0] if re.search(PATTERN, site) else [getWeather(site), 1]
def DevinateRes():
    return int(random.random()*4)

####主聊天功能
##學說話
def learn(lineMessage, channelId, e_source):
    lineMes = [x for x in lineMessage.replace("；",";").split(';') if x != ""]
    #若語法正確才加入詞條
    if(len(lineMes)<3):
        return ["窩聽不懂啦！", 0, 'text']
    else:
        insStatement(lineMes[1], lineMes[2:], channelId, e_source.type)
        return ["好哦的喵～", 0, 'text']
##忘記
def forget(lineMessage, channelId):
    lineMes = [x for x in lineMessage.replace("；",";").split(';') if x != ""]
    #若語法正確才刪除詞條
    if(len(lineMes)<3):
        return ["窩聽不懂啦！", 0, 'text']
    else:
        delStatement(lineMes[1], lineMes[2:], channelId)
        return ["好哦的喵～", 0, 'text']
##壞壞，批次降低資料庫內本次回話的關鍵字權重
def bad(channelId):
    adjustPrio(queryReceived(channelId, 1)[0][0], queryReply(channelId, 1)[0][0], -2)
    return ["好哦的喵～", 0, 'text']
##回覆(隨機回覆)
def chat(lineMessage, channelId):
    rand = 1 if lineMessage[0:3]=='牛批貓' or lineMessage[0:2]=='抽籤' else 0
    firstIndex = 0 if not rand else 3 if lineMessage[0:3]=='牛批貓' else 2
    response = resStatement(lineMessage[firstIndex:], channelId, rand)
    boolean = 0 if response=="窩聽不懂啦！" else 1
    type = 'image' if response[0:8]=='https://' and any(x in response for x in ['.jpg','.jpeg','.png']) else 'text'
    return [response, boolean, type]
##成功回話時增加權重或加入新詞
def validReply(lineMessage, reply):
    adjustPrio(lineMessage, reply, 1)
##齊推
def echo2(lineMessage, channelId):
    if all(lineMessage!=x[0] or x[1]!='text' for x in queryReceived(channelId, 3)): return False
    elif queryReply(channelId, 1)[0][0]==lineMessage: return False
    else: return True
##你會說什麼
def allLearn(channelId):
    return allStatement(channelId)


####功能開關
def globaltalk(lineMessage, channelId):
    if lineMessage=="可以說別人教的話": editChannelGlobalTalk(channelId, 1)
    elif any(s in lineMessage for s in ["不可以說別人教的話", "不能說別人教的話"]): editChannelGlobalTalk(channelId, 0)
    return "好哦的喵～"
def mute(lineMessage, channelId):
    if any(s in lineMessage for s in ["牛批貓說話", "牛批貓講話"]): editChannelMute(channelId, 0)
    elif any(s in lineMessage for s in ["牛批貓安靜", "牛批貓閉嘴"]): editChannelMute(channelId, 1)
    return "好哦的喵～"
def currentStatus(channelId):
    status = queryUser(channelId)
    return ["所有人教的" if status[2] else "這裡教的", "安靜" if status[3] else "可以說話", status[2], status[3]]
