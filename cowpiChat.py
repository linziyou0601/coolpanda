import sqlite3
from datetime import datetime

def createTable():
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE if not exists statements(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT NOT NULL,
                response TEXT NOT NULL,
                create_at TEXT NOT NULL,
                creator_id TEXT NOT NULL,
                channel_type TEXT NOT NULL
            )
        ''')

def insStatement(key, res, id, type):
    createTable()
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        for v in res:
            sql = 'INSERT INTO statements(keyword, response, create_at, creator_id, channel_type) VALUES(?,?,?,?,?)'
            c.execute(sql, [key, v, str(datetime.now()), id, type])

def resStatement(key):
    with sqlite3.connect('db/cowpi.db') as conn:
        c = conn.cursor()
        c.execute('SELECT response FROM statements Where keyword=%s limit 1', key)
        data = c.fetchall()
        return data[0][0]