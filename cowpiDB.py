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
                "creator_id" TEXT NOT NULL,
                "channel_type" TEXT NOT NULL,
                "priority" INTEGER DEFAULT 5
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS "received" (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "message" TEXT NOT NULL,
                "channel_id" TEXT NOT NULL
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS "reply" (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "message" TEXT NOT NULL,
                "channel_id" TEXT NOT NULL
            )
        ''')

##########[建立, 刪除, 更新, 查詢]: [聊天頻道資料]##########
def newChannel(channelId):
    createTable()
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM users Where channel_id=?', [channelId])
        if len(c.fetchall())>0:
            sql = 'INSERT INTO users(channel_id) VALUES(?)'
            c.execute(sql, [channelId])
def delChannel(channelId):
    createTable()
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        sql = 'DELETE FROM users Where channel_id=?'
        c.execute(sql, [channelId])
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
def queryUser(channelId):
    createTable()
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM users Where channel_id=?', [channelId])
        data = c.fetchall()
        return data[0] if len(data) else []

##########[儲存, 查詢]: [收到的訊息, 回覆]##########
def storeReceived(msg, channelId):
    createTable()
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        sql = 'INSERT INTO received(message, channel_id) VALUES(?,?)'
        c.execute(sql, [msg, channelId])
def storeReply(msg, channelId):
    createTable()
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        sql = 'INSERT INTO reply(message, channel_id) VALUES(?,?)'
        c.execute(sql, [msg, channelId])
def queryReceived(channelId, num):
    createTable()
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        c.execute('SELECT message FROM received Where channel_id=? ORDER BY id DESC limit ?', [channelId, num])
        data = c.fetchall()
        return [x[0] for x in data] if len(data) else [""]
def queryReply(channelId, num):
    createTable()
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        c.execute('SELECT message FROM reply Where channel_id=? ORDER BY id DESC limit ?', [channelId, num])
        data = c.fetchall()
        return [x[0] for x in data] if len(data) else [""]

##########[學說話, 刪除, 壞壞, 取得回覆]##########
def insStatement(key, msg, channelId, type):
    createTable()
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        for res in msg:
            sql = 'INSERT INTO statements(keyword, response, create_at, creator_id, channel_type) VALUES(?,?,?,?,?)'
            c.execute(sql, [key, res, str(datetime.now()), channelId, type])
def delStatement(key, msg, channelId):
    createTable()
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        for res in msg:
            c.execute('DELETE FROM statements Where keyword=? and response=? and creator_id=?', [key, res, channelId])
def adjustPrio(msg, case):
    createTable()
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        c.execute('SELECT keyword, response, priority FROM statements Where response=?', [msg])
        data = c.fetchall()
        for x in data:
            c.execute('UPDATE statements SET priority=? Where keyword=? and response=?', [int(x[2])+case, x[0], x[1]])
def resStatement(key, channelId):
    createTable()
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        c.execute('SELECT response FROM statements Where keyword=? and creator_id=? ORDER BY priority DESC, id DESC limit 1', [key, channelId])
        data = c.fetchall()
        if len(data)==0 and queryUser(channelId)[1]:
            c.execute('SELECT response FROM statements Where keyword=? ORDER BY priority DESC, id DESC limit 1', [key])
            data = c.fetchall()
        return data[0][0] if len(data) else "窩聽不懂啦！"