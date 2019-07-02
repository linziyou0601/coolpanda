from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ifvbkjtshpsxqj:4972b22ed367ed7346b0107d3c3e97db14fac1dde628cd6d7f08cf502c927ee1@ec2-50-16-197-244.compute-1.amazonaws.com:5432/d6tkud0mtknjov'
	
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class UserData(db.Model):
    __tablename__ = 'UserData'
	
    Id = db.Column(db.Integer, primary_key=True)
    KeyWord = db.Column(db.String(255))
    Description = db.Column(db.String(255))

    def __init__(self, KeyWord, Description):
        self.KeyWord = KeyWord
        self.Description = Description

    def __repr__(self):
        return "<UserData('%s', '%s')>" % (self.KeyWord, self.Description)

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
        add_data = UserData(KeyWord=keymessage, Description=message)
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