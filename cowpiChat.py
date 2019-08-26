import sqlite3
from datetime import datetime

def insStatement(key, res, id, type):
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
        for v in res:
            sql = 'INSERT INTO statements(keyword, response, create_at, creator_id, channel_type) VALUES('+ key +','+ v +','+ str(datetime.now()) +','+ id +','+ type +')'
            c.execute(sql)