def all(channelId):
if lineMessage == "所有籤桶" or lineMessage == "所有籤筒":
    content = ""
    sql = "SELECT topic from rndtopic;"
    cur.execute(sql)
    if cur.rowcount:
        keyList = list(dict.fromkeys([record[0] for record in cur.fetchall()]))
        conn.close()
        content = "【籤桶列表】\n"
        for row in keyList:
            content = content + row + "\n"
    else:
        content = "唉呀，沒有任何籤桶！"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=content))
    return 0

#新增籤桶內容
elif lineMessage.replace("；",";")[0:3] == "籤桶;" or lineMessage.replace("；",";")[0:3] == "籤筒;":
    lineMes = lineMessage.replace("；",";").split(';')
    keymessage = lineMes[1]
    if excludeWord(keymessage, event) == 1:
        for message in lineMes[2:]:
            sql = "SELECT topic from rndtopic where topic=%s and lottery=%s;"
            cur.execute(sql,(keymessage, message))
            if not cur.rowcount:
                sql = "INSERT INTO rndtopic (topic, lottery, channelId) VALUES(%s, %s, %s);"
                cur.execute(sql, (keymessage, message, channelId))
                conn.commit()
        conn.close()
        content = "我拿到了新的籤"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

#刪除籤桶內容
elif lineMessage.replace("；",";")[0:5] == "刪除籤桶;" or lineMessage.replace("；",";")[0:4] == "刪除籤筒;":
    lineMes = lineMessage.replace("；",";").split(';')
    keymessage = lineMes[1]
    if excludeWord(keymessage, event) == 1:
        sql = "DELETE FROM rndtopic WHERE topic=%s;"
        cur.execute(sql, (keymessage,))
        conn.commit()
        conn.close()
        content = "我把這桶籤給全吃了"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

#刪除籤桶
elif lineMessage.replace("；",";")[0:3] == "刪除;":
    lineMes = lineMessage.replace("；",";").split(';')
    keymessage = lineMes[1]
    if excludeWord(keymessage, event) == 1:
        for message in lineMes[2:]:
            sql = "DELETE FROM rndtopic WHERE topic=%s AND lottery=%s;"
            cur.execute(sql, (keymessage, message))
            conn.commit()
        conn.close()
        content = "我把籤給仍了"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

#抽一支籤
elif lineMessage.replace("；",";")[0:3] == "抽籤;":
    lineMes = lineMessage.replace("；",";").split(';')
    keymessage = lineMes[1]
    content = ""
    sql = "SELECT lottery from rndtopic where topic=%s;"
    cur.execute(sql, (keymessage,))
    if cur.rowcount:
        DescList = [record[0] for record in cur.fetchall()]
        conn.close() 
        content = random.choice(DescList)
    else:
        content = "唉呀，沒有這桶籤！"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=content))
    return 0