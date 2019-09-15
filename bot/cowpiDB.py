##########聊天機器人，資料庫存取##########
from django.conf import settings
from datetime import datetime
import psycopg2, pytz, json

def getConnect():
    conn = psycopg2.connect(database="d6tkud0mtknjov", user="ifvbkjtshpsxqj", password="4972b22ed367ed7346b0107d3c3e97db14fac1dde628cd6d7f08cf502c927ee1", host="ec2-50-16-197-244.compute-1.amazonaws.com", port="5432")
    conn.autocommit = True
    return conn

##########[建立資料表]: [對話, 收到的訊息, 回覆]##########
def createTable():
    #sqlite3.connect(settings.BASE_DIR + '/db/cowpi.db')
    conn = getConnect()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS "users" (
            "id" SERIAL PRIMARY KEY,
            "channel_id" TEXT NOT NULL,
            "globaltalk" INTEGER NOT NULL DEFAULT 0,
            "mute" INTEGER NOT NULL DEFAULT 0
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS "statements" (
            "id" SERIAL PRIMARY KEY,
            "keyword" TEXT NOT NULL,
            "response" TEXT NOT NULL,
            "create_at" TEXT NOT NULL,
            "channel_id" TEXT NOT NULL,
            "channel_type" TEXT NOT NULL,
            "priority" INTEGER NOT NULL DEFAULT 5
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS "received" (
            "id" SERIAL PRIMARY KEY,
            "type" TEXT NOT NULL,
            "message" TEXT NOT NULL,
            "channel_id" TEXT NOT NULL,
            "create_at" TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS "reply" (
            "id" SERIAL PRIMARY KEY,
            "type" TEXT NOT NULL,
            "message" TEXT NOT NULL,
            "valid" INTEGER DEFAULT 0,
            "channel_id" TEXT NOT NULL,
            "create_at" TEXT NOT NULL
        )
    ''')
    conn.close()
    autoIfEmptyStatements()

##########[建立, 刪除, 更新, 查詢]: [聊天頻道資料]##########
##建立頻道資料
def newChannel(channelId):
    conn = getConnect()
    c = conn.cursor()
    c.execute('SELECT * FROM users Where channel_id=%s', [channelId])
    #若頻道資料不存在才建立
    if len(c.fetchall())==0:
        c.execute('INSERT INTO users(channel_id) VALUES(%s)', [channelId])
    conn.close()
##刪除頻道資料
def delChannel(channelId):
    conn = getConnect()
    c = conn.cursor()
    c.execute('DELETE FROM users Where channel_id=%s', [channelId])
    conn.close()
##修改頻道功能
def editChannelGlobalTalk(channelId, value):
    conn = getConnect()
    c = conn.cursor()
    c.execute('UPDATE users SET globaltalk=%s Where channel_id=%s', [value, channelId])
    conn.close()
def editChannelMute(channelId, value):
    conn = getConnect()
    c = conn.cursor()
    c.execute('UPDATE users SET mute=%s Where channel_id=%s', [value, channelId])
    conn.close()
##查詢頻道功能狀態
def queryUser(channelId):
    conn = getConnect()
    c = conn.cursor()
    c.execute('SELECT * FROM users Where channel_id=%s', [channelId])
    data = c.fetchall()
    conn.close()
    return data[0] if len(data) else []


##########[儲存, 查詢]: [收到的訊息, 機器人回覆]##########
##儲存收到的訊息
def storeReceived(msg, type, channelId):
    conn = getConnect()
    c = conn.cursor()
    c.execute('INSERT INTO received(type, message, channel_id, create_at) VALUES(%s,%s,%s,%s)', [type, msg, channelId, str(datetime.now(pytz.timezone("Asia/Taipei")))])
    conn.close()
##儲存機器人回覆
def storeReply(msg, valid, type, channelId):
    conn = getConnect()
    c = conn.cursor()
    c.execute('INSERT INTO reply(type, message, valid, channel_id, create_at) VALUES(%s,%s,%s,%s,%s)', [type, msg, valid, channelId, str(datetime.now(pytz.timezone("Asia/Taipei")))])
    conn.close()
##查詢收到的訊息
def queryReceived(channelId, num):
    conn = getConnect()
    c = conn.cursor()
    c.execute('SELECT message, type FROM received Where channel_id=%s ORDER BY id DESC limit %s', [channelId, num])
    data = c.fetchall()
    conn.close()
    return [[x[0],x[1]] for x in data] if len(data) else [["",""]]
##查詢機器人回覆
def queryReply(channelId, num):
    conn = getConnect()
    c = conn.cursor()
    c.execute('SELECT message, valid, type FROM reply Where channel_id=%s ORDER BY id DESC limit %s', [channelId, num])
    data = c.fetchall()
    conn.close()
    return [[x[0],x[1],x[2]] for x in data] if len(data) else [["",0,""]]


##########[新增, 刪除, 調整權重, 取得回覆]: [詞條]##########
##新增詞條
def insStatement(key, msg, channelId, type):
    conn = getConnect()
    c = conn.cursor()
    for res in msg:
        c.execute('SELECT * FROM statements Where keyword=%s and response=%s and channel_id=%s', [key, res, channelId])
        #若詞條不存在於當前聊天室，才新增詞條
        if not len(c.fetchall()):
            c.execute('INSERT INTO statements(keyword, response, create_at, channel_id, channel_type) VALUES(%s,%s,%s,%s,%s)',
                        [key, res, str(datetime.now(pytz.timezone("Asia/Taipei"))), channelId, type])
        #若詞條存在於當前聊天室，則權重+1
        else: adjustPrio(key, res, 1, channelId)  
    conn.close()
##刪除詞條
def delStatement(key, msg, channelId):
    conn = getConnect()
    c = conn.cursor()
    for res in msg:
        c.execute('DELETE FROM statements Where keyword=%s and response=%s and channel_id=%s', [key, res, channelId])
    conn.close()
##調整詞條權重
def adjustPrio(key, msg, case, channelId=''):
    conn = getConnect()
    c = conn.cursor()
    listN = [msg]
    strKeyword = ''
    strChannelId = ''
    #若有指定channelId（手動加詞學習），則加入channelId條件；若為降低優先度，則不論keyword全一起降
    if case>0:
        strKeyword = ' and keyword=%s'
        listN.append(key)
    if channelId:
        strChannelId = ' and channel_id=%s'
        listN.append(channelId)
    c.execute('SELECT priority FROM statements Where response=%s' +strKeyword +strChannelId, listN)
    data = c.fetchall()
    #若詞條找不到，表示此句為自動接話模型、或廣泛搜尋模型，則增加一句自動學習詞條
    if len(data):
        for x in data:
            c.execute('UPDATE statements SET priority=%s Where response=%s' +strKeyword +strChannelId, [int(x[0])+case]+listN)
    else: insStatement(key, [msg], 'cowpi', 'autoLearn')
    conn.close()
##取得詞條回覆
def resStatement(key, channelId, rand):
    conn = getConnect()
    c = conn.cursor()
    #若關閉可以說其他人教過的話的功能，則以限制channelId的方式查詢
    strGlobaltalk = '' if queryUser(channelId)[2] else ' and channel_id=%s'
    strRandomreply = ' and priority>=5 ORDER BY RANDOM() limit 1' if rand else ' ORDER BY likestrong DESC, priority DESC, id DESC limit 1'
    c.execute('''
        SELECT response FROM ( SELECT *,
                                CASE
                                    WHEN keyword = %s THEN 5 
                                    WHEN %s LIKE '_' || keyword || '_' THEN 4
                                    WHEN %s LIKE '%' || keyword || '%' THEN 3
                                    WHEN keyword LIKE %s THEN 2
                                    WHEN keyword LIKE %s THEN 1
                                    ELSE 0 
                                END as likestrong
                        FROM statements) as foo Where likestrong>1''' + strGlobaltalk + strRandomreply, 
        [key, key, key, '_'+key+'_', '%'+key+'%'] if queryUser(channelId)[2] else [key, key, key, '_'+key+'_', '%'+key+'%', channelId]
    )
    data = c.fetchall()
    #找不到的話找找看自動學習的語料
    if not len(data):
        c.execute('''
            SELECT response FROM ( SELECT *,
                                    CASE
                                        WHEN keyword = %s THEN 5 
                                        WHEN %s LIKE '_' || keyword || '_' THEN 4
                                        WHEN %s LIKE '%' || keyword || '%' THEN 3
                                        WHEN keyword LIKE %s THEN 2
                                        WHEN keyword LIKE %s THEN 1
                                        ELSE 0 
                                    END as likestrong
                            FROM statements) as foo Where likestrong>0 and channel_id='cowpi' and priority>=5 ORDER BY RANDOM() limit 1''', 
            [key, key, key, '_'+key+'_', '%'+key+'%']
        )
        data = c.fetchall()
    conn.close()
    return data[0][0] if len(data) else "窩聽不懂啦！"
##取得所有學過的詞
def allStatement(channelId):
    conn = getConnect()
    c = conn.cursor()
    c.execute('SELECT keyword, response FROM statements Where channel_id=%s ORDER BY keyword', [channelId])
    data = c.fetchall()
    #建立回傳物件
    status = queryUser(channelId)
    ResCount = 0
    resData = {}
    dt = datetime.now(pytz.timezone("Asia/Taipei"))
    for x in data:
        ResCount+=1
        if x[0] in resData: resData[x[0]].append(x[1])
        else: resData[x[0]]=[x[1]]
    keyCount=len(resData)
    conn.close()
    #回傳物件
    return [
        "所有人教的" if status[2] else "這裡教的",
        "安靜" if status[3] else "可以說話",
        keyCount,
        ResCount,
        datetime.strftime(dt, '%Y{y}%m{m}%d{d} %H:%M').format(y='年', m='月', d='日'),
        resData if len(data) else "Null"
    ]




###################################初始語料資料###################################
def autoIfEmptyStatements():
    conn = getConnect()
    c = conn.cursor()
    c.execute('SELECT * FROM statements')
    if not len(c.fetchall()):
        with open('initKeyword.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        for k, v in data:
            for x in v:
                c.execute('INSERT INTO statements(keyword, response, create_at, channel_id, channel_type, priority) VALUES(%s,%s,%s,%s,%s,%s)',
                [k, x, str(datetime.now(pytz.timezone("Asia/Taipei"))), 'cowpi', 'autoLearn', 10])
    conn.close()
