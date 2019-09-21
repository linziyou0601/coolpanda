# import 必要的函式庫
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os, json, codecs, re
from .flexmessageFunc import *
from .chatterFunc import *
from .cowpiDB import *

line_bot_api = LineBotApi('HRWbC4w2S3J3JvFAQQkQnp4gxXVWtCwLWgrdanU72Y26+hwAoZvdiwhjyLPuIPdYLaqqy4ZDIC48EDGEo9FDp0VhS453OJfXEfFCwoFhZxhIFy6ESVLFr7fPuythQb4WA4gvEHkCjJ+yuMJDgzeR8gdB04t89/1O/w1cDnyilFU=')
parser = WebhookParser('4abb8726ea0ae9dc4a91154ce6fecb60')
handler = WebhookHandler('4abb8726ea0ae9dc4a91154ce6fecb60')

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
            createTable()
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
def handle_follow(event):
    newChannel(channelId = getChannelId(event))
    profile = line_bot_api.get_profile(event.source.user_id)
    content = TextSendMessage(text=profile.display_name + "，歡迎您成為本熊貓的好友" + sticon(u"\U00100097"))
    message = FlexSendMessage(alt_text="主選單", contents=flexMainMenu("main"))
    line_bot_api.reply_message(
        event.reply_token,
        [content, message])
    return 0
def handle_join(event):
    newChannel(channelId = getChannelId(event))
    content = TextSendMessage(text="大家好我叫牛批熊貓" + sticon(u"\U00100097"))
    message = FlexSendMessage(alt_text="主選單", contents=flexMainMenu("main"))
    line_bot_api.reply_message(
        event.reply_token,
        [content, message])
    return 0
def handle_unfollow(event):
    delChannel(channelId = getChannelId(event))
    return 0
def handle_leave(event):
    delChannel(channelId = getChannelId(event))
    return 0

####################訊息接收及回覆區####################
"""
【會自動學習的可能組合】
[（文字A）→（文字回答A／關鍵字回答A／圖片回答A）→（文字B）→（文字回答B／關鍵字回答B／圖片回答B）]
[（文字A）→（文字回答A／關鍵字回答A／圖片回答A）→（貼圖B／位置B）→（貼圖回答B／位置回答B）]
[（貼圖A／位置A）→（貼圖回答A／位置回答A）→（文字B）→（文字回答B／關鍵字回答B／圖片回答B）]
[（貼圖A／位置A）→（貼圖回答A／位置回答A）→（貼圖B／位置B）→（貼圖回答B／位置回答B）]

##加權模型所有組合
O [（文字A）→（文字回答A／關鍵字回答A／圖片回答A）] ※設 文字回答A==valid
X [（貼圖A／位置A）→（貼圖回答A／位置回答A）]

##接話模型所有組合
O [（文字回答A）→（文字B）] ※設 all([文字回答A, 所有回答B]==valid) && all([文字回答A, 所有回答B]!=關鍵字)
X [（文字回答A）→（貼圖B／位置B）]
X [（關鍵字回答A／圖片回答A／貼圖回答A／位置回答A）→（文字B／貼圖B／位置B）]

##同義模型所有組合
O [（文字A）→（文字回答B／關鍵字回答B／圖片回答B）] ※設 文字回答A==不懂 && 所有回答B==valid
X [（文字A）→（貼圖回答B／位置回答B）]
X [（貼圖A／位置A）→（文字回答B／關鍵字回答B／圖片回答B／貼圖回答B／位置回答B）]
"""
##回覆列表
replyList = []

##自動學習模型
def autoLearnModel(msg, content, channelId, event):
    if content[1]:
        #【加權模型】若 本次回答==valid 則學習 [文字A → 文字回答A／關鍵字回答A／圖片回答A]
        validReply(msg, content[0]) 
        #【接話模型】若 all(上次回答、本次回答==valid) && all(上次回答、本次回答!=關鍵字) && 上次回答類型==文字 則學習 [文字回答A → 文字B]
        if queryReply(channelId, 1)[0][2]=='text' and queryReply(channelId, 1)[0][1]==1 and content[1]==1:
            validReply(queryReply(channelId, 1)[0][0], msg)
        #【同義模型】若 上次回答==聽不懂 && 本次回答==valid 則學習 [文字A → 文字回答B／關鍵字回答B／圖片回答B]
        if queryReply(channelId, 1)[0][0]=='窩聽不懂啦！':
            validReply(queryReceived(channelId, 1)[0][0], content[0])

#關鍵字正則
def getReg(msg):
    RegDict = {
        "aqi":"(空[氣汙]|空氣(品質|如何|怎樣)|PM2.5|pm2.5)$",
        "weather":"(天氣|天氣(狀況|如何)|(會|有)下雨嗎)$",
        "divinate":"擲筊"
    }
    return RegDict[msg]

##關鍵字類型
def keyRes(msg, channelId, event):
    global replyList
    #空氣指標
    if re.search(getReg('aqi'), msg) and re.split(getReg('aqi'), msg)[0]!="": 
        key = AQI(re.split(getReg('aqi'), msg)[0].replace("台","臺"))
        if key!="":
            replyList = flexAQI(key)
            return True
    #天氣狀況
    elif re.search(getReg('weather'), msg) and re.split(getReg('weather'), msg)[0]!="": 
        key = Weather(re.split(getReg('weather'), msg)[0].replace("台","臺"))
        if key[0]!="":
            replyList = flexWeather(key[0]) if key[1] else flexWeather72HR(key[0])
            return True
    #擲筊
    elif msg == getReg('divinate'): 
        replyList = flexDevinate(DevinateRes())
        return True
    return False

def handle_message(event):
    channelId = getChannelId(event)
    newChannel(channelId) #新建頻道資料

    ##取得收到的訊息
    lineMessageType = event.message.type
    lineMessage = ""
    global replyList
    replyList = ""
    content=["", 0, ""]
    
    ##收到文字訊息
    if lineMessageType == 'text':
        lineMessage = event.message.text
        #####聊天回答第一階段#####功能型
        if lineMessage == "主選單" or lineMessage == "牛批貓":
            replyList = FlexSendMessage(alt_text="主選單", contents=flexMainMenu())
            content=[lineMessage, 0, 'flex']
        elif any(s == lineMessage for s in ["抽籤教學", "怎麼抽籤", "抽籤"]):
            replyList = FlexSendMessage(alt_text="如何隨機抽回答", contents=flexTeachLottery())
            content=[lineMessage, 0, 'flex']
        elif any(s == lineMessage for s in ["學說話教學", "怎麼學說話", "學說話", "教你說話"]):
            replyList = FlexSendMessage(alt_text="如何教我說話", contents=flexTeachChat())
            content=[lineMessage, 0, 'flex']
        elif any(s == lineMessage for s in (x+y for x in ["怎麼查", "如何查", "查"] for y in ["天氣", "空氣", "氣象"])):
            replyList = FlexSendMessage(alt_text="如何查氣象", contents=flexTeachCWB())
            content=[lineMessage, 0, 'flex']
        elif any(s == lineMessage for s in ["牛批貓會做什麼", "牛批貓會幹嘛", "你會幹嘛", "你會做什麼"]):
            replyList = FlexSendMessage(alt_text="我會哪些技能", contents=flexTeaching())
            content=[lineMessage, 0, 'flex']
        elif lineMessage == "目前狀態":
            replyList = flexStatusMenu(currentStatus(channelId))
            content=[lineMessage, 0, 'flex']
        elif lineMessage=="牛批貓會說什麼": #本聊天窗所有教過的東西
            replyList = flexWhatCanSay(allLearn(channelId))
            content=[lineMessage, 0, 'flex']
        elif "說別人教的話" in lineMessage: #回話資料庫開關
            replyList = TextSendMessage(text=globaltalk(lineMessage, channelId))
            content=[lineMessage, 0, 'text']
        elif any(s == lineMessage for s in ["牛批貓說話","牛批貓講話","牛批貓安靜", "牛批貓閉嘴"]): #安靜開關
            replyList = TextSendMessage(text=mute(lineMessage, channelId))
            content=[lineMessage, 0, 'text']
        elif not queryUser(channelId)[3]: #非安靜狀態
            #####聊天回答第二階段#####關鍵字類型
            if keyRes(lineMessage, channelId, event):
                content=[lineMessage, 2, 'flex']
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
                    content=[content[0], 2, 'flex']
                else:
                    #齊推
                    if not content[1] and echo2(lineMessage, channelId):
                        content = [lineMessage, 0, 'text']
                    #本次要回的話
                    if content[2]=='image':
                        replyList = ImageSendMessage(original_content_url=content[0], preview_image_url=content[0])
                    else:
                        replyList = TextSendMessage(text=content[0])
                
        ##自動學習
        autoLearnModel(lineMessage, content, channelId, event)
    
    ##收到貼圖
    elif lineMessageType == 'sticker':
        lineMessage = event.message.package_id + ',' + event.message.sticker_id
        replyList = StickerSendMessage(package_id=event.message.package_id, sticker_id=event.message.sticker_id)
        content=[lineMessage, 1, 'sticker'] 
    ##收到圖片、影片
    elif any(lineMessageType == x for x in ['image','video']):
        lineMessage = event.message.content_provider.original_content_url + ',' + event.message.content_provider.preview_image_url \
                      if event.message.content_provider.type=='external' else lineMessageType+'Message'
    ##收到音訊
    elif lineMessageType == 'audio':
        lineMessage = event.message.content_provider.original_content_url \
                      if event.message.content_provider.type=='external' else 'audioMessage'
    ##收到檔案
    elif lineMessageType == 'file':
        lineMessage = event.message.file_name
    ##收到位置訊息
    elif lineMessageType == 'location':
        lineMessage = str(event.message.latitude) + ',' + str(event.message.longitude) + ',' + str(event.message.address)
        replyList = TextSendMessage(text='你的位置是 ' + event.message.address)
        content=['你的位置是 ' + event.message.address, 1, 'location']

    ##儲存訊息
    if content[0]:
        storeReply(content[0], content[1], content[2], channelId) #記錄機器人本次回的「文字訊息」、「訊息有效度」
    storeReceived(lineMessage, lineMessageType, channelId) #儲存本次收到的語句
    
    ####回傳給LINE
    line_bot_api.reply_message(
        event.reply_token,
        replyList)
    return 0