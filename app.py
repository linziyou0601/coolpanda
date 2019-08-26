from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton
)
import os
from MessageFunc import *
from chatterFunc import *
from cowpiDB import *

app = Flask(__name__)

line_bot_api = LineBotApi('HRWbC4w2S3J3JvFAQQkQnp4gxXVWtCwLWgrdanU72Y26+hwAoZvdiwhjyLPuIPdYLaqqy4ZDIC48EDGEo9FDp0VhS453OJfXEfFCwoFhZxhIFy6ESVLFr7fPuythQb4WA4gvEHkCjJ+yuMJDgzeR8gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('4abb8726ea0ae9dc4a91154ce6fecb60')
    
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        #print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

def sticon(unic):
    return codecs.decode(json.dumps(unic).strip('"'), 'unicode_escape')

@handler.add(FollowEvent)
def handle_follow(event):
    newChannel(event.source.user_id)
    profile = line_bot_api.get_profile(event.source.user_id)
    content = TextSendMessage(text=profile.display_name + "，歡迎您成為本熊貓的好友" + sticon(u"\U00100097"))
    message = FlexSendMessage(alt_text="主選單", contents=mainMenu("main"))
    line_bot_api.reply_message(
        event.reply_token,
        [content, message])
    return 0

#關鍵保留字
def excludeWord(msg, event):
    exList = ['主選單', '所有籤桶', '所有籤筒', '籤桶', '籤筒', '刪除', '刪除籤桶', '刪除籤筒', '抽籤教學']
    if msg in exList:
        content = "這句話不能說，很可怕！"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    return 1

####################訊息接收及回覆區####################
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    e_source = event.source
    channelId = e_source.room_id if e_source.type == "room" else e_source.group_id if e_source.type == "group" else e_source.user_id
    
    ##取得收到的訊息
    lineMessage = event.message.text
    replyList = []
    newChannel(channelId) #新建頻道資料

    ##功能型
    if lineMessage == "主選單":
        replyList.append(FlexSendMessage(alt_text="主選單", contents=mainMenu()))
    elif lineMessage == "抽籤教學":
        replyList.append(FlexSendMessage(alt_text="抽籤教學", contents=teachLottery()))
    elif lineMessage == "如何學說話":
        replyList.append(FlexSendMessage(alt_text="如何教我說話", contents=teachChat()))
    elif lineMessage == "目前狀態":
        replyList.append(FlexSendMessage(alt_text="目前狀態", contents=statusMenu(currentStatus(channelId))))
    else:
        ##功能開關、聊天
        content=""
        if lineMessage=="牛批貓會說什麼": #本聊天窗所有教過的東西
            content = globaltalk(lineMessage, channelId)
        elif "說別人教的話" in lineMessage: #回話資料庫開關
            content = globaltalk(lineMessage, channelId)
        elif any(s == lineMessage for s in ["牛批貓說話","牛批貓講話","牛批貓安靜", "牛批貓閉嘴"]): #安靜開關
            content = mute(lineMessage, channelId)
        elif lineMessage == "壞壞": #名詞拉黑
            content = bad(channelId)
        elif lineMessage.replace("；",";")[0:4] == "學說話;": #學說話
            content = learn(lineMessage, channelId, e_source)
        elif lineMessage.replace("；",";")[0:3] == "忘記;": #刪詞
            content = forget(lineMessage, channelId)
        else: #回覆(隨機回覆)
            content = "" if queryUser(channelId)[3] else chat(lineMessage, channelId)
        if echo2(lineMessage, channelId)!="" and content=="窩聽不懂啦！": #齊推
            content = echo2(lineMessage, channelId)
        ##自動學習
        listA=[lineMessage, content[1:4], content[0:12]] #自動學習關鍵字排除對應
        listB=["牛批貓會說什麼", "天是 ", "現在時間 (UTC+8)："] #自動學習關鍵字排除列表
        if all(s != queryReply(channelId, 1)[0] for s in ["好哦的喵～","窩聽不懂啦！"]) and all([i!=j for i, j in zip(listA, listB)]):
            autolearn(queryReply(channelId, 1)[0], lineMessage, channelId, e_source) #順序性對話自動加入詞條
        if content!="窩聽不懂啦！":
            validReply(lineMessage, content, channelId) #若有詞條資料，則回覆時權重+1
        ##儲存訊息
        replyList.append(TextSendMessage(text=content)) #本次要回的話
        storeReply(content, channelId) #記錄機器人本次回的話
        storeReceived(lineMessage, channelId) #儲存本次語句
    
    #回傳給LINE
    line_bot_api.reply_message(
        event.reply_token,
        replyList)
    return 0

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)