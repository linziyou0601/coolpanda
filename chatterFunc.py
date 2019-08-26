from cowpiDB import *
from datetime import datetime, timedelta

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
    response = ""
    timeKey = ['現在時間', '現在幾點']
    dateKey = ['天日期', '天幾號', '星期幾', '幾月幾']
    weekDay = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    keyDay = ['今天','明天','昨天','後天','前天']
    keyDelta = [0,1,-1,2,-2]
    dt = datetime.utcnow() + timedelta(hours = 8)
    #若問時間
    if any(s in lineMessage for s in timeKey):
        response = "現在時間 (UTC+8)：" + str(dt.hour) + ":" + str(dt.minute)
    #若問日期
    elif any(s in lineMessage for s in dateKey):
        tmp = [v for v in keyDay if v in lineMessage][0]
        dt += timedelta(days = keyDelta[keyDay.index(tmp)])
        response = tmp + "是 " + str(dt.year) + "年" + str(dt.month) + "月" + str(dt.day) + "日 " + weekDay[dt.weekday()]
    #正常回覆
    else:
        rand = 1 if lineMessage[0:3]=='牛批貓' or lineMessage[0:2]=='抽籤' else 0
        firstIndex = 0 if not rand else 3 if lineMessage[0:3]=='牛批貓' else 2
        response = resStatement(lineMessage, channelId, rand)
    return response
##成功回話時增加權重
def validReply(lineMessage, reply, channelId):
    adjustPrio(lineMessage, reply, 1, "" if queryUser(channelId)[2] else channelId)
##齊推
def echo2(lineMessage, channelId):
    if not lineMessage in queryReceived(channelId, 5): return ""
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
    return "說話模式："+("" if status[2] else "不")+"可以說別人教的話\n"+"說話狀態："+("安靜" if status[3] else "可以說話")
