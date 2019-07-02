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

app = Flask(__name__)

line_bot_api = LineBotApi('3FqgS+7t25swQhSrd+NzCgo485B3J+FdcZ8I/oEB913QywyVyaNYA2c5kQ2XLvABLaqqy4ZDIC48EDGEo9FDp0VhS453OJfXEfFCwoFhZxjya96KO8r3oOzEe3SXfxndi/m25G1QpLiJEpsYiKfTZQdB04t89/1O/w1cDnyilFU=')
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
	message = TextSendMessage(text='hello world')
    line_bot_api.reply_message(
        event.reply_token,
        message)


if __name__ == "__main__":
    app.run()
