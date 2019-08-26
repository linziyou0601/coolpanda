from cowpiDB import *

#學說話
def learn(lineMessage, channelId, e_source):
    lineMes = lineMessage.replace("；",";").split(';')
    #確認語法正確性
    if(len(lineMes)<2):
        return "聽不懂啦～"
    else:
        insStatement(lineMes[1], lineMes[2:], channelId, e_source.type) #插入資料庫
        return "好哦的喵～"

#回覆
def chat(lineMessage):
    return resStatement(lineMessage)

#齊推
def echo2(lineMessage, channelId):
    recent_received_texts = queryReceived(channelId, 5)
    if lineMessage not in recent_received_texts: return "" # 如果在 channel_id 最近沒人講過 received_text，就不回應
    last_reply_text = queryReply(channelId, 1)
    if last_reply_text==lineMessage: return ""  # 如果在 channel_id 上一句回應是 received_text，就不回應
    return lineMessage
