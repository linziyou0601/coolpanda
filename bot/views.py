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
    message = FlexSendMessage(alt_text="主選單", contents=mainMenu("main"))
    line_bot_api.reply_message(
        event.reply_token,
        [content, message])
    return 0
#@handler.add(JoinEvent)
def handle_join(event):
    newChannel(channelId = getChannelId(event))
    content = TextSendMessage(text="大家好我叫牛批熊貓" + sticon(u"\U00100097"))
    message = FlexSendMessage(alt_text="主選單", contents=mainMenu("main"))
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
        "aqi":"(空[氣汙]|空氣(品質|如何)|PM2.5|pm2.5)$"
    }
    return RegDict[msg]

####################訊息接收及回覆區####################
#@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    channelId = getChannelId(event)
    
    ##取得收到的訊息
    lineMessage = event.message.text
    replyList = []
    newChannel(channelId) #新建頻道資料
    rted=0
    ##關鍵字型
    if re.search(getReg('aqi'), lineMessage): #空氣指標
        key = AQI(re.split(getReg('aqi'), lineMessage)[0].replace("台","臺"))
        if key!="": replyList.append(FlexSendMessage(alt_text="空氣品質", contents=nowAQI(key)))
        rted=1
    if not rted:
        ##功能型
        if lineMessage == "主選單":
            replyList.append(FlexSendMessage(alt_text="主選單", contents=mainMenu()))
        elif any(s == lineMessage for s in ["抽籤教學", "怎麼抽籤", "抽籤"]):
            replyList.append(FlexSendMessage(alt_text="如何抽籤", contents=teachLottery()))
        elif any(s == lineMessage for s in ["學說話教學", "怎麼學說話", "學說話", "教你說話"]):
            replyList.append(FlexSendMessage(alt_text="如何教我說話", contents=teachChat()))
        elif any(s == lineMessage for s in ["怎麼查時間", "怎麼查日期", "查時間", "查日期"]):
            replyList.append(FlexSendMessage(alt_text="如何教我說話", contents=teachDatetime()))
        elif any(s == lineMessage for s in ["怎麼查空氣", "如何查空氣", "查空氣", "空氣品質"]):
            replyList.append(FlexSendMessage(alt_text="如何教我說話", contents=teachAQI()))
        elif lineMessage == "牛批貓會幹嘛":
            replyList.append(FlexSendMessage(alt_text="我會哪些技能", contents=teaching()))
        elif lineMessage == "目前狀態":
            replyList.append(FlexSendMessage(alt_text="目前狀態", contents=statusMenu(currentStatus(channelId))))
        elif lineMessage=="牛批貓會說什麼": #本聊天窗所有教過的東西
            replyList.append(FlexSendMessage(alt_text="我會說什麼", contents=whatCanSay(allLearn(channelId))))
        elif "說別人教的話" in lineMessage: #回話資料庫開關
            replyList.append(TextSendMessage(text=globaltalk(lineMessage, channelId)))
        elif any(s == lineMessage for s in ["牛批貓說話","牛批貓講話","牛批貓安靜", "牛批貓閉嘴"]): #安靜開關
            replyList.append(TextSendMessage(text=mute(lineMessage, channelId)))
        else:
            ##聊天功能
            content=["",0]
            if lineMessage == "壞壞": #名詞拉黑
                content = bad(channelId)
            elif lineMessage.replace("；",";")[0:4] == "學說話;": #學說話
                content = learn(lineMessage, channelId, event.source)
            elif lineMessage.replace("；",";")[0:3] == "忘記;": #刪詞
                content = forget(lineMessage, channelId)

            if content[0]!="好哦的喵～": #回覆(或隨機回覆)
                content = "" if queryUser(channelId)[3] else chat(lineMessage, channelId)
            if echo2(lineMessage, channelId)!="" and content=="窩聽不懂啦！": #齊推
                content = echo2(lineMessage, channelId)
            
            ##自動學習
            if queryReply(channelId, 1)[0][1] and content[1]: #若上一句是從資料庫撈出來的回覆，則順序性對話自動加入詞條
                autolearn(queryReply(channelId, 1)[0][0], lineMessage, channelId, event.source)
            if content[1]: #若有詞條資料，則回覆時權重+1
                validReply(lineMessage, content[0], channelId)
            if queryReply(channelId, 1)[0][0]=='窩聽不懂啦！' and content[1]: #若上一句回答的是聽不懂，本次有詞條，則將上次收到的關鍵字和本次的回答學習
                validReply(queryReceived(channelId, 1)[0], content[0], channelId)
            
            ##儲存訊息
            replyList.append(TextSendMessage(text=content[0])) #本次要回的話
            storeReply(content[0], content[1], channelId) #記錄機器人本次回的話
            storeReceived(lineMessage, channelId) #儲存本次語句
    
    
    ####回傳給LINE
    line_bot_api.reply_message(
        event.reply_token,
        replyList)
    return 0