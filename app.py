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
import os
import psycopg2

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

def excludeWord(msg, event):
    exList = ['目錄', '所有主題', '新增', '刪除', '刪除主題']
    if msg in exList:
        content = "這句話不能說，很可怕！"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    return 1

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    conn = psycopg2.connect(database="d6tkud0mtknjov", user="ifvbkjtshpsxqj", password="4972b22ed367ed7346b0107d3c3e97db14fac1dde628cd6d7f08cf502c927ee1", host="ec2-50-16-197-244.compute-1.amazonaws.com", port="5432")
    lineMessage = event.message.text
    if lineMessage[0:4] == "所有主題":
        sql = "SELECT KeyWord from userdata;"
        cur = conn.cursor()
        cur.execute(sql)
        keyList = list(dict.fromkeys([record[0] for record in cur.fetchall()]))
        conn.close()
        content = ""
        for row in keyList:
            content = content + row + "\n"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    elif lineMessage[0:2] == "新增":
        lineMes = lineMessage.split(';')
        keymessage = lineMes[1]
        if excludeWord(keymessage, event) == 1:
            for message in lineMes[2:]:
                cur = conn.cursor()
                sql = "INSERT INTO userdata (KeyWord, Description) VALUES(%s, %s);"
                cur.execute(sql, (keymessage, message))
                conn.commit()
            conn.close()
            content = "我知道但我不想說"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content))
            return 0
    elif lineMessage[0:4] == "刪除主題":
        lineMes = lineMessage.split(';')
        keymessage = lineMes[1]
        if excludeWord(keymessage, event) == 1:
            cur = conn.cursor()
            sql = "DELETE FROM userdata WHERE KeyWord=%s;"
            cur.execute(sql, (keymessage,))
            conn.commit()
            conn.close()
            content = "我把這些垃圾給全吃了"
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
                sql = "DELETE FROM userdata WHERE KeyWord=%s AND Description=%s;"
                cur.execute(sql, (keymessage, message))
                conn.commit()
            conn.close()
            content = "我把這些垃圾給吃了"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content))
            return 0
    else:
        sql = "SELECT KeyWord from userdata;"
        cur = conn.cursor()
        cur.execute(sql)
        keyList = list(dict.fromkeys([record[0] for record in cur.fetchall()]))
        temp = ""
        for row in keyList:
            if row in lineMessage and len(row) >= len(temp):
                temp = row if row == lineMessage or len(row) > len(temp) else temp
        
        if temp != "":
            sql = "SELECT Description from userdata where KeyWord=%s;"
            cur = conn.cursor()
            cur.execute(sql, (temp,))
            DescList = [record[0] for record in cur.fetchall()]
            conn.close()
            content = ""
            for row in DescList:
                content = content + row + "\n"
            content = content + event.source.user_id
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content))
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=lineMessage))
            
        return 0

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)