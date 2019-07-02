from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from dModel import *

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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    lineMessage = event.message.text
    if lineMessage[0:4] == "加入選項":
        lineMes = lineMessage.split(';')
        keymessage = lineMes[1]
        excludeWord = ['目錄', '吃什麼']
        if keymessage in excludeWord:
            content = "這句話不能說，很可怕！"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content))
            return 0
        message = lineMes[2]
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=message))
        add_data = UserData(
            KeyWord=keymessage,
            Description=message
        )
        db.session.add(add_data)
        db.session.commit()
        db.session.close()

        content = "我知道但我不想說"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    else:
        message = TextSendMessage(text=event.message.text)
        line_bot_api.reply_message(event.reply_token, message)
    
#@handler.add(MessageEvent, message=TextMessage)
#def handle_message(event):
#    message = TextSendMessage(text=event.message.text)
#    line_bot_api.reply_message(event.reply_token, message)


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)