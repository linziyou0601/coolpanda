import sqlite3
from datetime import datetime

def createTable():
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
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

##[儲存, 查詢]: [收到的訊息, 回覆]
def storeReceived(msg, channelID):
    createTable()
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        sql = 'INSERT INTO received(message, channel_id) VALUES(?,?)'
        c.execute(sql, [msg, channelID])
def storeReply(msg, channelID):
    createTable()
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        sql = 'INSERT INTO reply(message, channel_id) VALUES(?,?)'
        c.execute(sql, [msg, channelID])
def queryReceived(channelID, num):
    createTable()
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        c.execute('SELECT message FROM received Where channel_id=? ORDER BY id DESC limit ?', [channelID, num])
        data = c.fetchall()
        return [x[0] for x in data]
def queryReply(channelID, num):
    createTable()
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        c.execute('SELECT message FROM reply Where channel_id=? ORDER BY id DESC limit ?', [channelID, num])
        data = c.fetchall()
        return [x[0] for x in data]

##[學說話, 取得回覆]
def insStatement(key, res, id, type):
    createTable()
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        for v in res:
            sql = 'INSERT INTO statements(keyword, response, create_at, creator_id, channel_type, priority) VALUES(?,?,?,?,?,?)'
            c.execute(sql, [key, v, str(datetime.now()), id, type, 5])
def resStatement(key):
    createTable()
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        c.execute('SELECT response FROM statements Where keyword=? ORDER BY id DESC limit 1', [key])
        data = c.fetchall()
        return data[0][0] if c.rowcount else "窩聽不懂啦！"