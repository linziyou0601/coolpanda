import sqlite3

def createDB():
    with sqlite3.connect('db/cowpi.sqlite3') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE statements(
                id INTEGER AUTOINCREMENT,
                keyword TEXT NOT NULL,
                response TEXT NOT NULL,
                create_at TEXT NOT NULL,
                creator_id TEXT NOT NULL,
                channel_type TEXT NOT NULL
            )
        ''')