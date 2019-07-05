from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
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
from chatbot import LineChatBOT

app = Flask(__name__)

line_bot_api = LineBotApi('HRWbC4w2S3J3JvFAQQkQnp4gxXVWtCwLWgrdanU72Y26+hwAoZvdiwhjyLPuIPdYLaqqy4ZDIC48EDGEo9FDp0VhS453OJfXEfFCwoFhZxhIFy6ESVLFr7fPuythQb4WA4gvEHkCjJ+yuMJDgzeR8gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('4abb8726ea0ae9dc4a91154ce6fecb60')

def msgFunc(stri):
    if stri=="main":
        return BubbleContainer(
                    direction='ltr',
                    hero=ImageComponent(
                        url='https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png',
                        size='full',
                        aspect_ratio='20:13',
                        aspect_mode='cover',
                        action=URIAction(uri='http://linecorp.com/', label='label')
                    ),
                    body=BoxComponent(
                        layout='vertical',
                        contents=[
                            # title
                            TextComponent(text='本大貓主選單', weight='bold', size='xl'),
                            # info
                            BoxComponent(
                                layout='vertical',
                                margin='lg',
                                spacing='sm',
                                contents=[
                                    BoxComponent(
                                        layout='baseline',
                                        spacing='sm',
                                        contents=[
                                            TextComponent(
                                                text='功能',
                                                color='#aaaaaa',
                                                size='sm',
                                                flex=2
                                            ),
                                            TextComponent(
                                                text='簡易聊天機器人、抽籤',
                                                wrap=True,
                                                color='#666666',
                                                size='sm',
                                                flex=4
                                            )
                                        ],
                                    ),
                                    BoxComponent(
                                        layout='baseline',
                                        spacing='sm',
                                        contents=[
                                            TextComponent(
                                                text='維護時間',
                                                color='#aaaaaa',
                                                size='sm',
                                                flex=2
                                            ),
                                            TextComponent(
                                                text="我爽就維護(◕ܫ◕)",
                                                wrap=True,
                                                color='#666666',
                                                size='sm',
                                                flex=4,
                                            ),
                                        ],
                                    ),
                                ],
                            )
                        ],
                    ),
                    footer=BoxComponent(
                        layout='vertical',
                        spacing='sm',
                        contents=[
                            ButtonComponent(
                                style='link',
                                height='sm',
                                action=MessageAction(
                                    label='所有籤桶',
                                    text='所有籤桶'
                                ),
                            ),
                            #SeparatorComponent(),
                            ButtonComponent(
                                style='link',
                                height='sm',
                                action=MessageAction(
                                    label='查看抽籤教學',
                                    text='抽籤教學'
                                ),
                            ),
                            SpacerComponent(size='sm')
                        ],
                        flex=0
                    ),
                )
    elif stri=="teach":
        return BubbleContainer(
                    direction='ltr',
                    hero=ImageComponent(
                        url='https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png',
                        size='full',
                        aspect_ratio='20:13',
                        aspect_mode='cover',
                        action=URIAction(uri='http://linecorp.com/', label='label')
                    ),
                    body=BoxComponent(
                        layout='vertical',
                        contents=[
                            # title
                            TextComponent(text='抽籤教學', weight='bold', size='xl'),
                            # info
                            BoxComponent(
                                layout='vertical',
                                margin='lg',
                                spacing='sm',
                                contents=[
                                    BoxComponent(
                                        layout='baseline',
                                        spacing='sm',
                                        contents=[
                                            TextComponent(
                                                text='注意',
                                                color='#aaaaaa',
                                                size='sm',
                                                flex=1
                                            ),
                                            TextComponent(
                                                text='其他聊天室新增的籤也會顯示！',
                                                wrap=True,
                                                color='#666666',
                                                size='sm',
                                                flex=5
                                            )
                                        ],
                                    )
                                ],
                            )
                        ],
                    ),
                    footer=BoxComponent(
                        layout='vertical',
                        spacing='sm',
                        contents=[
                            ButtonComponent(
                                style='link',
                                height='sm',
                                action=MessageAction(
                                    label='① 加入籤',
                                    text='籤桶;籤桶名稱;甲子籤;乙丑籤;丙寅籤;丁卯籤;戊辰籤'
                                ),
                            ),
                            ButtonComponent(
                                style='link',
                                height='sm',
                                action=MessageAction(
                                    label='② 抽一支籤',
                                    text='抽籤;籤桶名稱'
                                ),
                            ),
                            ButtonComponent(
                                style='link',
                                height='sm',
                                action=MessageAction(
                                    label='③ 刪除籤',
                                    text='刪除;籤桶名稱;甲子籤;丁卯籤'
                                ),
                            ),
                            ButtonComponent(
                                style='link',
                                height='sm',
                                action=MessageAction(
                                    label='④ 刪除籤桶',
                                    text='刪除籤桶;籤桶名稱'
                                ),
                            ),
                            ButtonComponent(
                                style='link',
                                height='sm',
                                action=MessageAction(
                                    label='主選單',
                                    text='主選單'
                                ),
                            ),
                            SpacerComponent(size='sm')
                        ],
                        flex=0
                    ),
                )
    
@app.route("/callback", methods=['POST'])
def callback():
    global bot
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    if bot == None:
        bot = LineChatBOT()

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
    message = FlexSendMessage(alt_text="hello", contents=msgFunc("main"))
    line_bot_api.reply_message(
        event.reply_token,
        [content, message])
    return 0

def excludeWord(msg, event):
    exList = ['主選單', '所有籤桶', '所有籤筒', '籤桶', '籤筒', '刪除', '刪除籤桶', '刪除籤筒', '抽籤教學']
    if msg in exList:
        content = "這句話不能說，很可怕！"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    return 1

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global bot
    conn = psycopg2.connect(database="linebotMain", user="postgres", password="Mm552288369", host="35.229.229.112", port="5432")
    lineMessage = event.message.text
    if lineMessage == "主選單":
        message = FlexSendMessage(alt_text="hello", contents=msgFunc("main"))
        line_bot_api.reply_message(
            event.reply_token,
            message)
        return 0
    elif lineMessage == "抽籤教學":
        message = FlexSendMessage(alt_text="hello", contents=msgFunc("teach"))
        line_bot_api.reply_message(
            event.reply_token,
            message)
        return 0
    elif lineMessage[0:4] == "所有籤桶" or lineMessage[0:4] == "所有籤筒":
        sql = "SELECT KeyWord from rndtopic;"
        cur = conn.cursor()
        cur.execute(sql)
        keyList = list(dict.fromkeys([record[0] for record in cur.fetchall()]))
        conn.close()
        content = ""
        for row in keyList:
            content = content + row + "\n"
        content = "唉呀，沒有籤桶！" if content == "" else content
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    elif lineMessage[0:2] == "籤桶" or lineMessage[0:2] == "籤筒":
        lineMes = lineMessage.split(';')
        keymessage = lineMes[1]
        if excludeWord(keymessage, event) == 1:
            for message in lineMes[2:]:
                cur = conn.cursor()
                sql = "INSERT INTO rndtopic (KeyWord, Description) VALUES(%s, %s);"
                cur.execute(sql, (keymessage, message))
                conn.commit()
            conn.close()
            content = "我拿到了新的籤"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content))
            return 0
    elif lineMessage[0:4] == "刪除籤桶" or lineMessage[0:4] == "刪除籤筒":
        lineMes = lineMessage.split(';')
        keymessage = lineMes[1]
        if excludeWord(keymessage, event) == 1:
            cur = conn.cursor()
            sql = "DELETE FROM rndtopic WHERE KeyWord=%s;"
            cur.execute(sql, (keymessage,))
            conn.commit()
            conn.close()
            content = "我把這桶籤給全吃了"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content))
            return 0
    elif lineMessage[0:2] == "刪除":
        lineMes = lineMessage.split(';')
        keymessage = lineMes[1]
        if excludeWord(keymessage, event) == 1:
            for message in lineMes[2:]:
                cur = conn.cursor()
                sql = "DELETE FROM rndtopic WHERE KeyWord=%s AND Description=%s;"
                cur.execute(sql, (keymessage, message))
                conn.commit()
            conn.close()
            content = "我把籤給仍了"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content))
            return 0
    elif lineMessage[0:2] == "抽籤":
        lineMes = lineMessage.split(';')
        keymessage = lineMes[1]
        cur = conn.cursor()
        sql = "SELECT Description from rndtopic where KeyWord=%s;"
        cur.execute(sql, (keymessage,))
        DescList = [record[0] for record in cur.fetchall()]
        conn.close() 
        content = random.choice(DescList)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    else:
        content = str(bot.getResponse(lineMessage))
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))  
        return 0

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)