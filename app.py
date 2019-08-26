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
import os, psycopg2, json, codecs, random
from MsgFunc import msgFunc
from cowpiFunc import learn, chat
from cowpiChat import insStatement, resStatement

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
    profile = line_bot_api.get_profile(event.source.user_id)
    content = TextSendMessage(text=profile.display_name + "，歡迎您成為本熊貓的好友" + sticon(u"\U00100097"))
    message = FlexSendMessage(alt_text="主選單", contents=msgFunc("main"))
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
    
    #取得收到的訊息
    lineMessage = event.message.text
    replyList = []
    ####功能型回覆
    if lineMessage == "主選單":
        message = FlexSendMessage(alt_text="主選單", contents=msgFunc("main"))
        line_bot_api.reply_message(
            event.reply_token,
            message)
        return 0
    elif lineMessage == "抽籤教學":
        message = FlexSendMessage(alt_text="抽籤教學", contents=msgFunc("teach"))
        line_bot_api.reply_message(
            event.reply_token,
            message)
        return 0
    elif lineMessage == "如何學說話":
        message = FlexSendMessage(alt_text="如何教我說話", contents=msgFunc("howToTrain"))
        line_bot_api.reply_message(
            event.reply_token,
            message)
        return 0

    ###抽籤
    #所有籤桶
    # elif lineMessage == "所有籤桶" or lineMessage == "所有籤筒":
    #     content = ""
    #     sql = "SELECT topic from rndtopic;"
    #     cur.execute(sql)
    #     if cur.rowcount:
    #         keyList = list(dict.fromkeys([record[0] for record in cur.fetchall()]))
    #         conn.close()
    #         content = "【籤桶列表】\n"
    #         for row in keyList:
    #             content = content + row + "\n"
    #     else:
    #         content = "唉呀，沒有任何籤桶！"
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         TextSendMessage(text=content))
    #     return 0

    # #新增籤桶內容
    # elif lineMessage.replace("；",";")[0:3] == "籤桶;" or lineMessage.replace("；",";")[0:3] == "籤筒;":
    #     lineMes = lineMessage.replace("；",";").split(';')
    #     keymessage = lineMes[1]
    #     if excludeWord(keymessage, event) == 1:
    #         for message in lineMes[2:]:
    #             sql = "SELECT topic from rndtopic where topic=%s and lottery=%s;"
    #             cur.execute(sql,(keymessage, message))
    #             if not cur.rowcount:
    #                 sql = "INSERT INTO rndtopic (topic, lottery, channelId) VALUES(%s, %s, %s);"
    #                 cur.execute(sql, (keymessage, message, channelId))
    #                 conn.commit()
    #         conn.close()
    #         content = "我拿到了新的籤"
    #         line_bot_api.reply_message(
    #             event.reply_token,
    #             TextSendMessage(text=content))
    #         return 0

    # #刪除籤桶內容
    # elif lineMessage.replace("；",";")[0:5] == "刪除籤桶;" or lineMessage.replace("；",";")[0:4] == "刪除籤筒;":
    #     lineMes = lineMessage.replace("；",";").split(';')
    #     keymessage = lineMes[1]
    #     if excludeWord(keymessage, event) == 1:
    #         sql = "DELETE FROM rndtopic WHERE topic=%s;"
    #         cur.execute(sql, (keymessage,))
    #         conn.commit()
    #         conn.close()
    #         content = "我把這桶籤給全吃了"
    #         line_bot_api.reply_message(
    #             event.reply_token,
    #             TextSendMessage(text=content))
    #         return 0

    # #刪除籤桶
    # elif lineMessage.replace("；",";")[0:3] == "刪除;":
    #     lineMes = lineMessage.replace("；",";").split(';')
    #     keymessage = lineMes[1]
    #     if excludeWord(keymessage, event) == 1:
    #         for message in lineMes[2:]:
    #             sql = "DELETE FROM rndtopic WHERE topic=%s AND lottery=%s;"
    #             cur.execute(sql, (keymessage, message))
    #             conn.commit()
    #         conn.close()
    #         content = "我把籤給仍了"
    #         line_bot_api.reply_message(
    #             event.reply_token,
    #             TextSendMessage(text=content))
    #         return 0

    # #抽一支籤
    # elif lineMessage.replace("；",";")[0:3] == "抽籤;":
    #     lineMes = lineMessage.replace("；",";").split(';')
    #     keymessage = lineMes[1]
    #     content = ""
    #     sql = "SELECT lottery from rndtopic where topic=%s;"
    #     cur.execute(sql, (keymessage,))
    #     if cur.rowcount:
    #         DescList = [record[0] for record in cur.fetchall()]
    #         conn.close() 
    #         content = random.choice(DescList)
    #     else:
    #         content = "唉呀，沒有這桶籤！"
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         TextSendMessage(text=content))
    #     return 0

    #學說話
    elif lineMessage.replace("；",";")[0:4] == "學說話;":
        content = learn(lineMessage, channelId, e_source)
        replyList.append(content)

    #回覆
    else:
        content = chat(lineMessage)
        replyList.append(content)
    
    line_bot_api.reply_message(
        event.reply_token,
        replyList)
    return 0

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)