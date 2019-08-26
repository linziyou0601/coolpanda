from MsgFunc import msgFunc
from cowpiChat import insStatement, resStatement

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