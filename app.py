from flask import Flask, request, abort
from flask_cors import cross_origin
from urllib.parse import parse_qs
import os, json, codecs, re, random

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

#導入env, model
from env import *
from model import *
#導入Others
from Others.flexMessageJSON import *
#導入Controllers
from Controllers.normalController import *
from Controllers.chatterController import *
from Controllers.keyController import *
#導入Services
from Services.crawlerService import *
from Services.lotteryService import *
from Services.autoLearnService import *
from Services.geocodingService import *

app = Flask(__name__)

line_bot_api = LineBotApi(GET_SECRET("ACCESS_TOKEN")) 
handler = WebhookHandler(GET_SECRET("API_SECRET"))

####################檢查uWSGI->Flask是否正常運作####################
@app.route("/")
def index():
    return 'BotApp is Working!'

####################一般callback####################
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        create_table()
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

####################推播####################
@app.route("/pushing", methods=['POST'])
def pushing():
    data = json.loads(request.get_data())
    mtype = data.get('type', 'text')
    title = data.get('title', '')
    message = data.get('message', '')
    channel_id = data.get('channel_id', '')
    template = data.get('template', None)
    status = pushing_process(mtype, title, message, channel_id) if template == None else pushing_template(title, message, channel_id, template)
    return json.dumps({'msg': status})

####################小功能####################
##隨機產生後綴字
def getPostfix():
    p = random.randint(1,10)
    postfix = get_postfix() if get_postfix() and p%5==0 else ""
    return postfix

#貼圖unicode轉line編碼 [請傳入 sticon(u"\U數字") ]
def sticon(unic):
    return codecs.decode(json.dumps(unic).strip('"'), 'unicode_escape')

#取得ChannelId [如果是群組或聊天室，一樣回傳channelId，不是userId]
def getChannelId(event):
    e_source = event.source
    return e_source.room_id if e_source.type == "room" else e_source.group_id if e_source.type == "group" else e_source.user_id

#取得UserId
def getUserId(event):
    return event.source.user_id if hasattr(event.source, 'user_id') else None

####################[匯入, 拉黑, JSON]: [詞條]####################
#詞條拉黑
@app.route("/operateStatement", methods=['POST'])
def operateStatement():
    data = json.loads(request.get_data())
    action = data["action"]
    adjust = data["adjust"]
    statement_id = data["statement_id"]
    operate_statement(action, adjust, statement_id)
    return json.dumps({'msg': 'ok'})

#匯入詞條
@app.route("/importStatement", methods=['POST'])
def importStatement():
    data = json.loads(request.get_data())
    for item in data["data"]:
        create_statement(item["keyword"], item["response"], "autoLearn", "autoLearn")
    return json.dumps({'msg': 'ok'})

#詞條轉JSON
@app.route("/getStatementJSON", methods=['POST'])
def getStatementJSON():
    data = json.loads(request.get_data())
    channel_id = data["channel_id"] if data["channel_id"] and data["channel_id"]!="ALL" else "ALL"
    return json.dumps(get_line_statement_table(channel_id))

#推播紀錄轉JSON
@app.route("/getPushedJSON", methods=['POST'])
def getPushedJSON():
    return json.dumps(get_line_pushed_table())

####################取得EVENT物件、發送訊息####################
def get_event_obj(event):
    ##取得頻道及使用者ID
    channelId = getChannelId(event)
    userId = getUserId(event)
    ##建頻道資料
    if userId: create_channel(userId)
    create_channel(channelId)
    ##取得頻道資料
    channelData = get_channel(channelId)
    userData = get_channel(userId) if userId else None
    
    profileName = ""
    try: profileName = line_bot_api.get_profile(userId).display_name if userId else ""
    except: profileName = ""

    return {
        "reply_token": event.reply_token,
        "channelId": channelId,
        "userId": userId,
        "lineMessage": "",                              #取得收到的訊息
        "lineMessageType": event.message.type if hasattr(event, 'message') else None,
        "level": int(int(userData['exp'])/10) if userData else int(int(channelData['exp'])/10),     #等級
        "exp": int(userData['exp'])%10 if userData else int(channelData['exp'])%10,          #經驗值每+10升一級
        "nickname": userData['nickname'] if userData and int(int(userData['exp'])/10)>=2 and userData['nickname'] else profileName,
        "mute": channelData['mute'],
        "global_talk": channelData['global_talk'],
        "replyList": [],                                #初始化傳送內容（可為List或單一Message Object）
        "replyLog": ["", 0, ""],                        #發出去的物件準備寫入紀錄用 [訊息, 有效度(0=功能型, 1=關鍵字, 2=一般型), 訊息類型]
        "postfix": getPostfix()
    }
def send_reply(GET_EVENT, STORE_LOG = False):
    ##儲存訊息
    if STORE_LOG:
        if GET_EVENT["replyLog"][0]: store_replied(GET_EVENT["replyLog"][0], GET_EVENT["replyLog"][1], GET_EVENT["replyLog"][2], GET_EVENT["channelId"])  #記錄機器人本次回的訊息
        store_received(GET_EVENT["lineMessage"], GET_EVENT["lineMessageType"], GET_EVENT["channelId"], GET_EVENT["userId"])                               #儲存本次收到的語句
    ####回傳給LINE
    line_bot_api.reply_message(GET_EVENT["reply_token"], GET_EVENT["replyList"])

####################[加入, 退出]: [好友, 聊天窗]####################
@handler.add(FollowEvent)
def handle_follow(event):
    ##取得EVENT物件
    GET_EVENT = get_event_obj(event)
    flexObject = flexStatusMenu(current_status(GET_EVENT))
    GET_EVENT["replyList"] = [
        TextSendMessage(text=GET_EVENT["nickname"] + "，歡迎您成為本熊貓的好友！" + sticon(u"\U00100097")),
        FlexSendMessage(alt_text = "主選單", contents = flexMainMenu(GET_EVENT["channelId"], GET_EVENT["level"])),
        FlexSendMessage(alt_text = flexObject[0], contents = flexObject[1])
    ]
    ##發送回覆
    send_reply(GET_EVENT, False)

@handler.add(JoinEvent)
def handle_join(event):
    ##取得EVENT物件
    GET_EVENT = get_event_obj(event)
    flexObject = flexStatusMenu(current_status(GET_EVENT))
    GET_EVENT["replyList"] = [
        TextSendMessage(text="大家好我叫酷熊貓" + sticon(u"\U00100097")),
        FlexSendMessage(alt_text = "主選單", contents = flexMainMenu(GET_EVENT["channelId"], GET_EVENT["level"])),
        FlexSendMessage(alt_text = flexObject[0], contents = flexObject[1])
    ]
    ##發送回覆
    send_reply(GET_EVENT, False)

@handler.add(UnfollowEvent)
def handle_unfollow(event):
    remove_channel(getChannelId(event))

@handler.add(LeaveEvent)
def handle_leave(event):
    remove_channel(getChannelId(event))

####################PostbackEvent處理區#################### 
@handler.add(PostbackEvent)
def handle_postback(event):
    ##取得EVENT物件
    GET_EVENT = get_event_obj(event)
    data = parse_qs(event.postback.data)
    ##確認詞條內容
    if data['action'][0]=='confirm_learn':
        temp_statement = get_temp_statement(data['id'][0])
        if temp_statement:
            create_statement(temp_statement['keyword'], [temp_statement['response']], temp_statement['channel_id'], temp_statement['user_id'])
            adjust_exp(temp_statement['user_id'], 1)
            GET_EVENT["replyList"] = TextSendMessage(text="好哦已新增～"+GET_EVENT['postfix'])
    ##放棄詞條內容
    if data['action'][0]=='cancel_learn':
        temp_statement = get_temp_statement(data['id'][0])
        if temp_statement:
            delete_temp_statement(data['id'][0])
            GET_EVENT["replyList"] = TextSendMessage(text="已放棄新增～"+GET_EVENT['postfix'])
    
    ##傳送地點內容
    if data['action'][0]=='get_map':
        GET_EVENT["replyList"] = LocationSendMessage(title=data['title'][0], address=data['addr'][0], latitude=data['lat'][0], longitude=data['lng'][0])
    
    ##擲筊
    if data['action'][0]=='devinate':
        flexObject = flexDevinate(getDevinate())
        GET_EVENT["replyList"] = FlexSendMessage(alt_text = flexObject[0], contents = flexObject[1])
    ##抽籤詩
    if data['action'][0]=='fortuneStick':
        flexObject = flexFortuneStick(getFortuneStick())
        GET_EVENT["replyList"] = FlexSendMessage(alt_text = flexObject[0], contents = flexObject[1]) 
    ##籤解
    if data['action'][0]=='meaning_fortuneStick':
        flexObject = flexMeaningFortuneStick(getMeaningFortuneStick(int(data['id'][0])))
        GET_EVENT["replyList"] = FlexSendMessage(alt_text = flexObject[0], contents = flexObject[1])
    ##抽塔羅
    if data['action'][0]=='draw_tarot':
        flexObject = flexTarot(getTarot(int(data['num'][0])))
        GET_EVENT["replyList"] = FlexSendMessage(alt_text = flexObject[0], contents = flexObject[1])
    ##塔羅牌義
    if data['action'][0]=='meaning_tarot':
        flexObject = flexMeaningTarot(getMeaningTarot(int(data['id'][0])))
        GET_EVENT["replyList"] = FlexSendMessage(alt_text = flexObject[0], contents = flexObject[1])
    
    ##發送回覆
    send_reply(GET_EVENT, False)

####################文字訊息處理區#################### 
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    ##取得EVENT物件
    GET_EVENT = get_event_obj(event)
    GET_EVENT["lineMessage"] = event.message.text
    last_receives = get_received(GET_EVENT["channelId"], 5)

    ## ==================== 對答 ==================== ##
    #學說話 [不限個人, 等級0+]
    if any(key(s['message'])=="學說話" for s in last_receives[0:2]) or key(GET_EVENT["lineMessage"])=="學說話":
        if key(GET_EVENT["lineMessage"])=="學說話":
            GET_EVENT["replyList"] = FlexSendMessage(alt_text = "請告訴我要學的關鍵字", contents = flexTellMeKeyRes("請告訴我要學的關鍵字"))
            GET_EVENT["replyLog"] = ["請告訴我要學的關鍵字", 0, 'flex']
        elif key(last_receives[0]['message'])=="學說話":
            GET_EVENT["replyList"] = FlexSendMessage(alt_text = "我要回應什麼？", contents = flexTellMeKeyRes("我要回應什麼？"))
            GET_EVENT["replyLog"] = ["我要回應什麼？", 0, 'flex']
        else:
            temp_id = create_temp_statement(last_receives[0]['message'], GET_EVENT["lineMessage"], GET_EVENT["channelId"], last_receives[1]['user_id'])
            GET_EVENT["replyList"] = FlexSendMessage(alt_text = "確認詞條內容", contents = flexLearnConfirm(last_receives[0]['message'], GET_EVENT["lineMessage"], temp_id))
            GET_EVENT["replyLog"] = ["確認詞條內容", 0, 'flex']
    #降低詞條優先度 [不限個人, 等級0+]
    elif key(GET_EVENT["lineMessage"])=="壞壞":
        GET_EVENT["replyList"] = TextSendMessage(text=chat_bad(GET_EVENT["channelId"])+GET_EVENT["postfix"])
        GET_EVENT["replyLog"] = ["好哦～", 0, 'text']
    
    #指定暱稱 [個人, 等級2+]
    elif (any(key(s['message'])=="指定暱稱" for s in last_receives[0:1]) or key(GET_EVENT["lineMessage"])=="指定暱稱") and GET_EVENT["channelId"][0]=='U' and GET_EVENT["level"]>=2:
        if key(GET_EVENT["lineMessage"])=="指定暱稱":
            GET_EVENT["replyList"] = FlexSendMessage(alt_text = "要指定的暱稱是？", contents = flexTellMeNickname())
            GET_EVENT["replyLog"] = ["要指定的暱稱是？", 0, 'flex']
        else:
            set_nickname(GET_EVENT["lineMessage"], GET_EVENT["channelId"])
            GET_EVENT["replyList"] = FlexSendMessage(alt_text = "成功指定暱稱："+GET_EVENT["lineMessage"], contents = flexNicknameConfirm(GET_EVENT["lineMessage"]))
            GET_EVENT["replyLog"] = ["成功指定暱稱"+GET_EVENT["lineMessage"], 0, 'flex']
    #解除指定暱稱 [個人, 等級2+]
    elif key(GET_EVENT["lineMessage"])=="解除指定暱稱" and GET_EVENT["channelId"][0]=='U' and GET_EVENT["level"]>=2:
        GET_EVENT["replyList"] = TextSendMessage(text=set_nickname(None, GET_EVENT["channelId"])+GET_EVENT["postfix"])
        GET_EVENT["replyLog"] = ["好哦～", 0, 'text']


    ## ==================== 爬蟲查詢 ==================== ##
    #天氣查詢 [不限個人, 等級0+]    # 若上一句key值為「(目前天氣|未來天氣)$」且不為「地名(目前天氣|未來天氣)$」 或 本句key值為「(地名)*(目前天氣|未來天氣)$」
    elif any((re.search("(目前天氣|未來天氣)$", key(s['message'])) and not re.sub("(目前天氣|未來天氣)", "", key(s['message']))) for s in last_receives[0:1]) or re.search("(目前天氣|未來天氣)$", key(GET_EVENT["lineMessage"])):
        #若本語句中有問天氣
        if re.search("(目前天氣|未來天氣)$", key(GET_EVENT["lineMessage"])):
            future = True if "未來" in key(GET_EVENT["lineMessage"]) else False
            this_site = re.sub("(目前天氣|未來天氣)", "", key(GET_EVENT["lineMessage"]))
            #若本語句中有直接給地點
            if this_site:
                weather = getWeather(None, None, this_site, future)
                if weather:
                    flexObject = flexWeather72HR(weather) if future else flexWeather(weather)
                    GET_EVENT["replyList"] = FlexSendMessage(alt_text = flexObject[0], contents = flexObject[1])
                    GET_EVENT["replyLog"] = [flexObject[0], 0, 'flex']
            #問地點
            else:
                GET_EVENT["replyList"] = FlexSendMessage(alt_text = "請輸入要查詢的位址，或傳送位址訊息", contents = flexTellMeLocation())
                GET_EVENT["replyLog"] = ["要查詢的地點是？", 0, 'flex']
        #若上語句中有問天氣且沒給地點
        else:
            future = True if "未來" in key(last_receives[0]['message']) else False
            weather = getWeather(None, None, GET_EVENT["lineMessage"], future)
            if weather:
                flexObject = flexWeather72HR(weather) if future else flexWeather(weather)
                GET_EVENT["replyList"] = FlexSendMessage(alt_text = flexObject[0], contents = flexObject[1])
                GET_EVENT["replyLog"] = [flexObject[0], 0, 'flex']
    
    #空汙查詢 [不限個人, 等級0+]    # 若上一句key值為「(空汙查詢)$」且不為「地名(空汙查詢)$」 或 本句key值為「(地名)*(空汙查詢)$」
    elif any((re.search("(空汙查詢)$", key(s['message'])) and not re.sub("(空汙查詢)", "", key(s['message']))) for s in last_receives[0:1]) or re.search("(空汙查詢)$", key(GET_EVENT["lineMessage"])):
        #若本語句中有問空汙
        if re.search("(空汙查詢)$", key(GET_EVENT["lineMessage"])):
            this_site = re.sub("(空汙查詢)", "", key(GET_EVENT["lineMessage"]))
            #若本語句中有直接給地點
            if this_site:
                aqi = getAQI(None, None, this_site)
                if aqi:
                    flexObject = flexAQI(aqi)
                    GET_EVENT["replyList"] = FlexSendMessage(alt_text = flexObject[0], contents = flexObject[1])
                    GET_EVENT["replyLog"] = [flexObject[0], 0, 'flex']
            #問地點
            else:
                GET_EVENT["replyList"] = FlexSendMessage(alt_text = "請輸入要查詢的位址，或傳送位址訊息", contents = flexTellMeLocation())
                GET_EVENT["replyLog"] = ["要查詢的地點是？", 0, 'flex']
        #若上語句中有問空汙且沒給地點
        else:
            aqi = getAQI(None, None, GET_EVENT["lineMessage"])
            if aqi:
                flexObject = flexAQI(aqi)
                GET_EVENT["replyList"] = FlexSendMessage(alt_text = flexObject[0], contents = flexObject[1])
                GET_EVENT["replyLog"] = [flexObject[0], 0, 'flex']

    #特約藥局查詢 [不限個人, 等級0+]
    elif any(key(s['message'])=="特約藥局查詢" for s in last_receives[0:1]) or key(GET_EVENT["lineMessage"])=="特約藥局查詢":
        if key(GET_EVENT["lineMessage"])=="特約藥局查詢": 
            GET_EVENT["replyList"] = FlexSendMessage(alt_text = "請輸入要查詢的位址，或傳送位址訊息", contents = flexTellMeLocation())
            GET_EVENT["replyLog"] = ["要查詢的地點是？", 0, 'flex']
        else:
            mask_list = getMask(None, None, GET_EVENT["lineMessage"])
            if mask_list:
                GET_EVENT["replyList"] = [
                    TextSendMessage(text="以下是距離最近的10間藥局"),
                    FlexSendMessage(alt_text="以下是距離最近的10間藥局", contents = flexWhereMask(mask_list))
                ]
                GET_EVENT["replyLog"] = ["特約藥局查詢結果", 0, 'flex']


    ## ==================== 機率運勢 ==================== ##
    #擲筊選單 [不限個人, 等級0+] 
    elif key(GET_EVENT["lineMessage"])=="擲筊": 
        GET_EVENT["replyList"] = FlexSendMessage(alt_text= "擲筊選單", contents=flexMenuDevinate())
        GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 0, 'flex']
    #抽籤詩選單 [不限個人, 等級0+]
    elif key(GET_EVENT["lineMessage"])=="抽籤詩":
        GET_EVENT["replyList"] = FlexSendMessage(alt_text= "抽籤詩選單", contents=flexMenuFortuneStick())
        GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 0, 'flex']
    #抽塔羅選單 [不限個人, 等級0+]
    elif key(GET_EVENT["lineMessage"])=="抽塔羅":
        GET_EVENT["replyList"] = FlexSendMessage(alt_text= "抽塔羅選單", contents=flexMenuTarot())
        GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 0, 'flex']
    
    
    ## ==================== 教學選單 ==================== ##
    #主選單 [不限個人, 等級0+]
    elif key(GET_EVENT["lineMessage"])=="主選單":
        GET_EVENT["replyList"] = FlexSendMessage(alt_text = "主選單", contents = flexMainMenu(GET_EVENT["channelId"], GET_EVENT["level"]))
        GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 0, 'flex']
    #酷熊貓會做什麼選單 [不限個人, 等級0+]
    elif key(GET_EVENT["lineMessage"])=="功能一覽":
        GET_EVENT["replyList"] = FlexSendMessage(alt_text = "功能一覽", contents = flexHowDo(GET_EVENT["channelId"], GET_EVENT["level"]))
        GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 0, 'flex']
    #聊天教學選單 [不限個人, 等級0+] 
    elif key(GET_EVENT["lineMessage"])=="怎麼聊天": 
        GET_EVENT["replyList"] = FlexSendMessage(alt_text= "怎麼和我聊天", contents=flexTeachChat())
        GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 0, 'flex']
    #抽籤教學選單 [不限個人, 等級0+] 
    elif key(GET_EVENT["lineMessage"])=="怎麼抽籤": 
        GET_EVENT["replyList"] = FlexSendMessage(alt_text= "怎麼抽籤", contents=flexTeachLottery())
        GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 0, 'flex']

    #學說話教學選單 [不限個人, 等級0+] 
    elif key(GET_EVENT["lineMessage"])=="怎麼學說話": 
        GET_EVENT["replyList"] = FlexSendMessage(alt_text= "怎麼教我說話", contents=flexTeachLearn())
        GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 0, 'flex']
    #本聊天窗所有教過的東西 [不限個人, 等級0+]
    elif key(GET_EVENT["lineMessage"])=="學過的話":
        flexObject = flexWhatCanSay(chat_all_learn(GET_EVENT["channelId"], GET_EVENT["nickname"]))
        GET_EVENT["replyList"] = FlexSendMessage(alt_text= flexObject[0], contents=flexObject[1])
        GET_EVENT["replyLog"] = [flexObject[0], 0, 'flex']
    #抽籤式回答教學選單 [不限個人, 等級0+]
    elif key(GET_EVENT["lineMessage"])=="怎麼抽籤式回答":
        GET_EVENT["replyList"] = FlexSendMessage(alt_text= "怎麼抽籤式回答", contents=flexTeachChatRandom())
        GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 0, 'flex']

    #暱稱教學選單 [個人, 等級2+]
    elif key(GET_EVENT["lineMessage"])=="怎麼指定暱稱" and GET_EVENT["channelId"][0]=='U' and GET_EVENT["level"]>=2:
        GET_EVENT["replyList"] = FlexSendMessage(alt_text= "如何指定暱稱", contents=flexTeachNickname())
        GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 0, 'flex']
    #等級說明選單 [個人, 等級0+]
    elif key(GET_EVENT["lineMessage"])=="等級說明":
        GET_EVENT["replyList"] = FlexSendMessage(alt_text= "等級（經驗值）說明", contents=flexTeachLevel())
        GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 0, 'flex']

    #查氣象教學選單 [不限個人, 等級0+] 
    elif key(GET_EVENT["lineMessage"])=="怎麼查氣象": 
        GET_EVENT["replyList"] = FlexSendMessage(alt_text= "怎麼查氣象", contents=flexTeachMeteorology())
        GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 0, 'flex']
    #查天氣教學選單 [不限個人, 等級0+] 
    elif key(GET_EVENT["lineMessage"])=="怎麼查天氣": 
        GET_EVENT["replyList"] = FlexSendMessage(alt_text= "怎麼查天氣", contents=flexTeachWeather())
        GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 0, 'flex']
    #查空汙教學選單 [不限個人, 等級0+] 
    elif key(GET_EVENT["lineMessage"])=="怎麼查空汙": 
        GET_EVENT["replyList"] = FlexSendMessage(alt_text= "怎麼查空汙", contents=flexTeachAQI())
        GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 0, 'flex']
    #查藥局教學選單 [不限個人, 等級0+] 
    elif key(GET_EVENT["lineMessage"])=="怎麼查藥局": 
        GET_EVENT["replyList"] = FlexSendMessage(alt_text= "怎麼查藥局", contents=flexTeachMask())
        GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 0, 'flex']
    

    ## ==================== 功能設定 ==================== ##
    #目前等級 [個人, 等級0+]
    elif key(GET_EVENT["lineMessage"])=="目前等級":
        GET_EVENT["replyList"] = FlexSendMessage(alt_text= GET_EVENT["nickname"]+"的等級\nLv. "+str(GET_EVENT["level"])+"\n經驗值 "+str(GET_EVENT["exp"])+"/10", contents=flexLevelMenu(GET_EVENT["nickname"], GET_EVENT["level"], GET_EVENT["exp"]))
        GET_EVENT["replyLog"] = [GET_EVENT["nickname"]+"的等級\nLv. "+str(GET_EVENT["level"])+"\n經驗值 "+str(GET_EVENT["exp"])+"/10", 0, 'flex']
    #目前暱稱 [個人, 等級2+]
    elif key(GET_EVENT["lineMessage"])=="目前暱稱" and GET_EVENT["channelId"][0]=='U' and GET_EVENT["level"]>=2:
        nickname_text = GET_EVENT["nickname"] if GET_EVENT["nickname"] else "無"
        GET_EVENT["replyList"] = FlexSendMessage(alt_text= "目前暱稱："+nickname_text, contents=flexNicknameMenu(nickname_text))
        GET_EVENT["replyLog"] = ["目前暱稱："+nickname_text, 0, 'flex']
    #目前狀態 [不限個人, 等級0+]
    elif key(GET_EVENT["lineMessage"])=="目前狀態":
        flexObject = flexStatusMenu(current_status(GET_EVENT))
        GET_EVENT["replyList"] = FlexSendMessage(alt_text= flexObject[0], contents=flexObject[1])
        GET_EVENT["replyLog"] = [flexObject[0], 0, 'flex']
    #說話模式調整 [不限個人, 等級0+]
    elif key(GET_EVENT["lineMessage"])=="說話模式調整":
        GET_EVENT["replyList"] = TextSendMessage(text=global_talk(GET_EVENT["lineMessage"], GET_EVENT["channelId"])+GET_EVENT["postfix"])
        GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 0, 'text']
    #安靜開關 [不限個人, 等級0+]
    elif key(GET_EVENT["lineMessage"])=="聊天狀態調整":
        GET_EVENT["replyList"] = TextSendMessage(text=mute(GET_EVENT["lineMessage"], GET_EVENT["channelId"])+GET_EVENT["postfix"])
        GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 0, 'text']
    

    ## ==================== 聊天 ==================== ##
    elif not GET_EVENT['mute']: #非安靜狀態
        #資料庫回覆(或隨機回覆)
        GET_EVENT["replyLog"] = chat_response(GET_EVENT["lineMessage"], GET_EVENT["channelId"])
        #齊推
        if not GET_EVENT["replyLog"][1] and chat_echo2(GET_EVENT["lineMessage"], GET_EVENT["channelId"]):
            GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 0, 'text']
        #本次要回的話
        if GET_EVENT["replyLog"][2]=='image':
            GET_EVENT["replyList"] = ImageSendMessage(original_content_url=GET_EVENT["replyLog"][0], preview_image_url=GET_EVENT["replyLog"][0])
        else:
            GET_EVENT["replyList"] = TextSendMessage(text=GET_EVENT["replyLog"][0]+GET_EVENT["postfix"]) if GET_EVENT["replyLog"][0]!='我聽不懂啦！' or GET_EVENT["channelId"][0]=='U' else []

    ##自動學習
    auto_learn_model(GET_EVENT)
    ##發送
    send_reply(GET_EVENT, True)

####################貼圖訊息處理區#################### 
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    ##取得EVENT物件
    GET_EVENT = get_event_obj(event)
    GET_EVENT["lineMessage"] = event.message.package_id + ',' + event.message.sticker_id
    GET_EVENT["replyList"] = StickerSendMessage(package_id=event.message.package_id, sticker_id=event.message.sticker_id)
    GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 2, 'sticker']
    GET_EVENT["replyList"] = [GET_EVENT["replyList"], TextSendMessage(text=GET_EVENT["postfix"])] if GET_EVENT["postfix"] else GET_EVENT["replyList"]
    ##發送
    send_reply(GET_EVENT, True)

####################位置訊息處理區#################### 
@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    ##取得EVENT物件
    LOCATION_INFO = {
        "title": str(event.message.title),
        "addr": addr_format(str(event.message.address)),
        "lat": float(event.message.latitude),
        "lng": float(event.message.longitude)
    }
    GET_EVENT = get_event_obj(event)
    GET_EVENT["lineMessage"] = LOCATION_INFO["title"] + ',' + LOCATION_INFO["addr"] + ',' + str(LOCATION_INFO["lat"]) + ',' + str(LOCATION_INFO["lng"])
    last_receives = get_received(GET_EVENT["channelId"], 5)
    
    ##儲存地址資訊 
    create_location(LOCATION_INFO["addr"], LOCATION_INFO["lat"], LOCATION_INFO["lng"])
    
    #天氣查詢 [不限個人, 等級0+]    # 若上一句key值為「(目前天氣|未來天氣)$」且不為「地名(目前天氣|未來天氣)$」
    if any((re.search("(目前天氣|未來天氣)$", key(s['message'])) and not re.sub("(目前天氣|未來天氣)", "", key(s['message']))) for s in last_receives[0:1]):
        #若上語句中有問天氣且沒給地點
        future = True if "未來" in key(last_receives[0]['message']) else False
        flexObject = flexWeather72HR(getWeather(LOCATION_INFO["lat"], LOCATION_INFO["lng"], None, future)) if future else flexWeather(getWeather(LOCATION_INFO["lat"], LOCATION_INFO["lng"], None, future))
        GET_EVENT["replyList"] = FlexSendMessage(alt_text = flexObject[0], contents = flexObject[1])
        GET_EVENT["replyLog"] = [flexObject[0], 0, 'flex']

    #空汙查詢 [不限個人, 等級0+]    # 若上一句key值為「(空汙查詢)$」且不為「地名(空汙查詢)$」 或 本句key值為「(地名)*(空汙查詢)$」
    elif any((re.search("(空汙查詢)$", key(s['message'])) and not re.sub("(空汙查詢)", "", key(s['message']))) for s in last_receives[0:1]):
        #若上語句中有問空汙且沒給地點
        flexObject = flexAQI(getAQI(LOCATION_INFO["lat"], LOCATION_INFO["lng"], None))
        GET_EVENT["replyList"] = FlexSendMessage(alt_text = flexObject[0], contents = flexObject[1])
        GET_EVENT["replyLog"] = [flexObject[0], 0, 'flex']
    
    ##特約藥局查詢 [不限個人, 等級0+]
    elif any(key(s['message'])=="特約藥局查詢" for s in last_receives[0:1]):
        mask_list = getMask(LOCATION_INFO["lat"], LOCATION_INFO["lng"], None)
        GET_EVENT["replyList"] = [
            TextSendMessage(text="以下是距離最近的10間藥局"),
            FlexSendMessage(alt_text="以下是距離最近的10間藥局", contents = flexWhereMask(mask_list))
        ]
        GET_EVENT["replyLog"] = ["特約藥局查詢", 0, 'flex']

    ##發送
    send_reply(GET_EVENT, True)


if __name__ == "__main__":
    app.run()