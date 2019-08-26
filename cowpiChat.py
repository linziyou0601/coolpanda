import sqlite3
from datetime import datetime

def insStatement(key, res, id, type):
    with sqlite3.connect('db/cowpi.sqlite3') as conn:
        for v in res:
            c = conn.cursor()
            sql = '''
                INSERT INTO statements(keyword, response, create_at, creator_id, channel_type)
                VALUES('''+ key +''','''+ v +''','''+ str(datetime.now()) +''','''+ id +''','''+ type +''')
            '''
            c.execute(sql)