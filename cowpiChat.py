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
        c.execute('SELECT response FROM statements Where keyword=? ORDER BY id DESC limit 1', (key,))
        data = c.fetchall()
        return data[0][0] if c.rowcount else "窩聽不懂啦！"