# import 必要的函式庫
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os, json, codecs, re
from .messageFunc import *
from .chatterFunc import *
from .cowpiDB import *

line_bot_api = LineBotApi('HRWbC4w2S3J3JvFAQQkQnp4gxXVWtCwLWgrdanU72Y26+hwAoZvdiwhjyLPuIPdYLaqqy4ZDIC48EDGEo9FDp0VhS453OJfXEfFCwoFhZxhIFy6ESVLFr7fPuythQb4WA4gvEHkCjJ+yuMJDgzeR8gdB04t89/1O/w1cDnyilFU=')
parser = WebhookParser('4abb8726ea0ae9dc4a91154ce6fecb60')
handler = WebhookHandler('4abb8726ea0ae9dc4a91154ce6fecb60')

# @app.route("/callback", methods=['POST'])
# def callback():
#     # get X-Line-Signature header value
#     signature = request.headers['X-Line-Signature']

#     # get request body as text
#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)

#     # handle webhook body
#     try:
#         handler.handle(body, signature)
#     except InvalidSignatureError:
#         #print("Invalid signature. Please check your channel access token/channel secret.")
#         abort(400)

#     return 'OK'

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
            autoIfEmptyStatements()
        except InvalidSignatureError:
            return HttpResponseForbidden()

        for event in events:
            if isinstance(event, FollowEvent):
                handle_follow(event)
            if isinstance(event, JoinEvent):
                handle_join(event)
            if isinstance(event, UnfollowEvent):
                handle_unfollow(event)
            if isinstance(event, LeaveEvent):
                handle_leave(event)
            if isinstance(event, FollowEvent):
                handle_follow(event)
            if isinstance(event, MessageEvent):
                handle_message(event)
        return HttpResponse()
    else:
        return HttpResponseForbidden()


def sticon(unic):
    return codecs.decode(json.dumps(unic).strip('"'), 'unicode_escape')
def getChannelId(event):
    e_source = event.source
    return e_source.room_id if e_source.type == "room" else e_source.group_id if e_source.type == "group" else e_source.user_id 

####################[加入, 退出]: [好友, 聊天窗]####################
#@handler.add(FollowEvent)
def handle_follow(event):
    newChannel(channelId = getChannelId(event))
    profile = line_bot_api.get_profile(event.source.user_id)
    content = TextSendMessage(text=profile.display_name + "，歡迎您成為本熊貓的好友" + sticon(u"\U00100097"))
    message = FlexSendMessage(alt_text="主選單", contents=flexMainMenu("main"))
    line_bot_api.reply_message(
        event.reply_token,
        [content, message])
    return 0
#@handler.add(JoinEvent)
def handle_join(event):
    newChannel(channelId = getChannelId(event))
    content = TextSendMessage(text="大家好我叫牛批熊貓" + sticon(u"\U00100097"))
    message = FlexSendMessage(alt_text="主選單", contents=flexMainMenu("main"))
    line_bot_api.reply_message(
        event.reply_token,
        [content, message])
    return 0
#@handler.add(UnfollowEvent)
def handle_unfollow(event):
    delChannel(channelId = getChannelId(event))
    return 0
#@handler.add(LeaveEvent)
def handle_leave(event):
    delChannel(channelId = getChannelId(event))
    return 0

#關鍵保留字
def getReg(msg):
    RegDict = {
        "aqi":"(空[氣汙]|空氣(品質|如何)|PM2.5|pm2.5)$",
        "weather":"(天氣|天氣(狀況|如何)|會下雨嗎)$",
        "divinate":"擲筊",
    }
    return RegDict[msg]

####################訊息接收及回覆區####################
##回覆列表
replyList = []

##自動學習模型
def autoLearnModel(msg, content, channelId, event):
    if content[1]:
        validReply(msg, content[0]) #若有詞條資料，則回覆時權重+1，若無則學習
        if queryReply(channelId, 1)[0][1]==1 and content[1]!=2: #若上一句是從資料庫撈出來的回覆，且不是關鍵字回覆，則順序性對話自動加入詞條
            validReply(queryReply(channelId, 1)[0][0], msg)
        if queryReply(channelId, 1)[0][0]=='窩聽不懂啦！': #若上一句回答的是聽不懂，本次有詞條，則將上次收到的關鍵字和本次的回答學習
            validReply(queryReceived(channelId, 1)[0], content[0])

##關鍵字型
def keyRes(msg, channelId, event):
    global replyList
    #空氣指標
    if re.search(getReg('aqi'), msg) and re.split(getReg('aqi'), msg)[0]!="": 
        key = AQI(re.split(getReg('aqi'), msg)[0].replace("台","臺"))
        if key!="":
            replyList = FlexSendMessage(alt_text="空氣品質", contents=flexAQI(key))
            return True
    #天氣狀況
    elif re.search(getReg('weather'), msg) and re.split(getReg('weather'), msg)[0]!="": 
        key = Weather(re.split(getReg('weather'), msg)[0].replace("台","臺"))
        if key[0]!="":
            replyList = FlexSendMessage(alt_text="天氣狀況", contents=flexWeather(key[0]) if key[1] else flexWeather72HR(key[0]))
            return True
    #擲筊
    elif msg == getReg('divinate'): 
        replyList = FlexSendMessage(alt_text="擲筊結果", contents=flexDevinate(DevinateRes()))
        return True
    return False

#@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    channelId = getChannelId(event)
    
    ##取得收到的訊息
    lineMessage = event.message.text
    newChannel(channelId) #新建頻道資料
    global replyList
    content=["", 0]
    
    #####聊天回答第一階段#####功能型
    if lineMessage == "主選單" or lineMessage == "牛批貓":
        replyList = FlexSendMessage(alt_text="主選單", contents=flexMainMenu())
        content=[lineMessage, 0]
    elif any(s == lineMessage for s in ["抽籤教學", "怎麼抽籤", "抽籤"]):
        replyList = FlexSendMessage(alt_text="如何隨機抽回答", contents=flexTeachLottery())
        content=[lineMessage, 0]
    elif any(s == lineMessage for s in ["學說話教學", "怎麼學說話", "學說話", "教你說話"]):
        replyList = FlexSendMessage(alt_text="如何教我說話", contents=flexTeachChat())
        content=[lineMessage, 0]
    elif any(s == lineMessage for s in ["怎麼查時間", "怎麼查日期", "查時間", "查日期"]):
        replyList = FlexSendMessage(alt_text="如何查時間日期", contents=flexTeachDatetime())
        content=[lineMessage, 0]
    elif any(s == lineMessage for s in (x+y for x in ["怎麼查", "如何查", "查"] for y in ["天氣", "空氣", "氣象"])):
        replyList = FlexSendMessage(alt_text="如何查氣象", contents=flexTeachCWB())
        content=[lineMessage, 0]
    elif any(s == lineMessage for s in ["牛批貓會做什麼", "牛批貓會幹嘛", "你會幹嘛", "你會做什麼"]):
        replyList = FlexSendMessage(alt_text="我會哪些技能", contents=flexTeaching())
        content=[lineMessage, 0]
    elif lineMessage == "目前狀態":
        replyList = FlexSendMessage(alt_text="目前狀態", contents=flexStatusMenu(currentStatus(channelId)))
        content=[lineMessage, 0]
    elif lineMessage=="牛批貓會說什麼": #本聊天窗所有教過的東西
        replyList = FlexSendMessage(alt_text="我會說什麼", contents=flexWhatCanSay(allLearn(channelId)))
        content=[lineMessage, 0]
    elif "說別人教的話" in lineMessage: #回話資料庫開關
        replyList = TextSendMessage(text=globaltalk(lineMessage, channelId))
        content=[lineMessage, 0]
    elif any(s == lineMessage for s in ["牛批貓說話","牛批貓講話","牛批貓安靜", "牛批貓閉嘴"]): #安靜開關
        replyList = TextSendMessage(text=mute(lineMessage, channelId))
        content=[lineMessage, 0]
    elif not queryUser(channelId)[3]: #非安靜狀態
        #####聊天回答第二階段#####關鍵字類型
        if keyRes(lineMessage, channelId, event):
            content=[lineMessage, 2]
        else:
            #####聊天回答第三階段#####聊天類型
            if lineMessage == "壞壞": #名詞拉黑
                content = bad(channelId)
            elif lineMessage.replace("；",";")[0:4] == "學說話;": #學說話
                content = learn(lineMessage, channelId, event.source)
            elif lineMessage.replace("；",";")[0:3] == "忘記;": #刪詞
                content = forget(lineMessage, channelId)
            else: #資料庫回覆(或隨機回覆)
                content = chat(lineMessage, channelId)

            #最終反查關鍵字類型
            if keyRes(content[0], channelId, event):
                content=[content[0], 2]
            else:
                #齊推
                if echo2(lineMessage, channelId):
                    content = echo2(lineMessage, channelId)
                replyList = TextSendMessage(text=content[0]) #本次要回的話
    
    ##自動學習
    autoLearnModel(lineMessage, content, channelId, event)
    ##儲存訊息
    storeReply(content[0], content[1], channelId) #記錄機器人本次回的「文字訊息」、「訊息有效度」
    storeReceived(lineMessage, channelId) #儲存本次收到的語句
    
    ####回傳給LINE
    line_bot_api.reply_message(
        event.reply_token,
        replyList)
    return 0