import sqlite3
from datetime import datetime

##########[建立資料表]: [對話, 收到的訊息, 回覆]##########
def createTable():
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS "users" (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "channel_id" TEXT NOT NULL,
                "globaltalk" INTEGER NOT NULL DEFAULT 0,
                "mute" INTEGER NOT NULL DEFAULT 0
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS "statements" (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "keyword" TEXT NOT NULL,
                "response" TEXT NOT NULL,
                "create_at" TEXT NOT NULL,
                "channel_id" TEXT NOT NULL,
                "channel_type" TEXT NOT NULL,
                "priority" INTEGER DEFAULT 5
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS "received" (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "message" TEXT NOT NULL,
                "channel_id" TEXT NOT NULL,
                "create_at" TEXT NOT NULL
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS "reply" (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "message" TEXT NOT NULL,
                "channel_id" TEXT NOT NULL,
                "create_at" TEXT NOT NULL
            )
        ''')

##########[建立, 刪除, 更新, 查詢]: [聊天頻道資料]##########
##建立頻道資料
def newChannel(channelId):
    createTable()
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM users Where channel_id=?', [channelId])
        #若頻道資料已存在，則重複不建立
        if len(c.fetchall())==0:
            sql = 'INSERT INTO users(channel_id) VALUES(?)'
            c.execute(sql, [channelId])
##刪除頻道資料
def delChannel(channelId):
    createTable()
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        sql = 'DELETE FROM users Where channel_id=?'
        c.execute(sql, [channelId])
##修改頻道功能
def editChannelGlobalTalk(channelId, value):
    createTable()
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        sql = 'UPDATE users SET globaltalk=? Where channel_id=?'
        c.execute(sql, [value, channelId])
def editChannelMute(channelId, value):
    createTable()
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        sql = 'UPDATE users SET mute=? Where channel_id=?'
        c.execute(sql, [value, channelId])
##查詢頻道功能狀態
def queryUser(channelId):
    createTable()
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM users Where channel_id=?', [channelId])
        data = c.fetchall()
        return data[0] if len(data) else []


##########[儲存, 查詢]: [收到的訊息, 機器人回覆]##########
##儲存收到的訊息
def storeReceived(msg, channelId):
    createTable()
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        sql = 'INSERT INTO received(message, channel_id, create_at) VALUES(?,?,?)'
        c.execute(sql, [msg, channelId, str(datetime.now())])
##儲存機器人回覆
def storeReply(msg, channelId):
    createTable()
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        sql = 'INSERT INTO reply(message, channel_id, create_at) VALUES(?,?,?)'
        c.execute(sql, [msg, channelId, str(datetime.now())])
##查詢收到的訊息
def queryReceived(channelId, num):
    createTable()
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        c.execute('SELECT message FROM received Where channel_id=? ORDER BY id DESC limit ?', [channelId, num])
        data = c.fetchall()
        return [x[0] for x in data] if len(data) else [""]
##查詢機器人回覆
def queryReply(channelId, num):
    createTable()
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        c.execute('SELECT message FROM reply Where channel_id=? ORDER BY id DESC limit ?', [channelId, num])
        data = c.fetchall()
        return [x[0] for x in data] if len(data) else [""]


##########[新增, 刪除, 調整權重, 取得回覆]: [詞條]##########
##新增詞條
def insStatement(key, msg, channelId, type):
    createTable()
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM statements where keyword=?, response=?, channel_id=?', [key, msg, channelId])
        #若詞條存在於當前聊天室，則權重+1
        if len(c.fetchall())!=0:
            adjustPrio(key, msg, 1, channelId)
        #若詞條不存在，則新增詞條
        else:
            for res in msg:
                sql = 'INSERT INTO statements(keyword, response, create_at, channel_id, channel_type) VALUES(?,?,?,?,?)'
                c.execute(sql, [key, res, str(datetime.now()), channelId, type])
##刪除詞條
def delStatement(key, msg, channelId):
    createTable()
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        for res in msg:
            c.execute('DELETE FROM statements Where keyword=? and response=? and channel_id=?', [key, res, channelId])
##調整詞條權重
def adjustPrio(key, msg, case, channelId=""):
    createTable()
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        #若有指定channelId，則加入channelId條件
        c.execute('SELECT priority FROM statements Where keyword=? and response=?' + ' and channel_id=?' if channelId!="" else '',
                  [key, msg, channelId] if channelId!="" else [key, msg])
        if len(c.fetchall())!=0:
            c.execute('UPDATE statements SET priority=? Where keyword=? and response=?' + ' and channel_id=?' if channelId!="" else '',
                      [int(c.fetchall()[0][0])+case, key, msg, channelId] if channelId!="" else [int(c.fetchall()[0][0])+case, key, msg])
##取得詞條回覆
def resStatement(key, channelId):
    createTable()
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        c.execute('SELECT response FROM statements Where keyword=? and channel_id=? ORDER BY priority DESC, id DESC limit 1', [key, channelId])
        data = c.fetchall()
        #若有開啟可以說其他人教過的話的功能，則加入查詢
        if len(data)==0 and queryUser(channelId)[1]:
            c.execute('SELECT response FROM statements Where keyword=? ORDER BY priority DESC, id DESC limit 1', [key])
            data = c.fetchall()
        return data[0][0] if len(data) else "窩聽不懂啦！"