from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

##主選單
def flexMainMenu(arg=[]):
    return {
        "type": "bubble", "direction": "ltr",
        "hero": { "type": "image", "url": "https://i.imgur.com/kW0Fr2H.png", "size": "full", "aspectRatio": "20:13", "aspectMode": "cover" },
        "body": {
            "type": "box", "layout": "vertical",
            "contents": [
                { "type": "text", "text": "牛批熊貓主選單", "size": "xl", "weight": "bold" },
                {
                    "type": "box", "layout": "baseline", "margin": "lg",
                    "contents": [
                        { "type": "text", "text": "功能", "size": "sm", "flex": 2, "color": "#aaaaaa" },
                        { "type": "text", "text": "胡言亂語、抽籤、擲筊、查氣象、查時間", "wrap": True, "flex": 4, "size": "sm", "color": "#666666" }
                    ]
                },
                {
                    "type": "box", "layout": "baseline",
                    "contents": [
                        { "type": "text", "text": "維護時間", "size": "sm", "flex": 2, "color": "#aaaaaa" },
                        { "type": "text", "text": "我爽就維護(◕ܫ◕)", "wrap": True, "flex": 4, "size": "sm", "color": "#666666" }
                    ]
                }
            ]
        },
        "footer": {
            "type": "box", "layout": "vertical",
            "contents": [
                { "type": "separator", "margin": "xxl" },
                {
                    "type": "button", "style": "link", "height": "sm",
                    "action": { "type": "message", "label": "功能教學", "text": "牛批貓會幹嘛" }
                },
                {
                    "type": "button", "style": "link", "height": "sm",
                    "action": { "type": "message", "label": "我要擲筊", "text": "擲筊" }
                },
                {
                    "type": "button", "style": "link", "height": "sm",
                    "action": { "type": "message", "label": "目前狀態", "text": "目前狀態" }
                }
            ]
        }
    }

##抽籤式回應教學
def flexTeachLottery(arg=[]):
    return {
        "type": "bubble", "direction": "ltr",
        "body": {
            "type": "box", "layout": "vertical",
            "contents": [
                # title
                { "type": "text", "text": "教學", "color": "#1DB446", "size": "sm", "weight": "bold" },
                { "type": "text", "text": "抽籤式回覆", "margin": "md", "size": "xxl", "weight": "bold" },
                # info
                {
                    "type": "box", "layout": "baseline", "margin": "md",
                    "contents": [
                        { "type": "text", "text": "注意", "color": "#AAAAAA", "size": "sm", "flex": 1 },
                        { "type": "text", "text": "若有開啟「可以說別人教的話」的功能，則也會從其他聊天室教的詞條隨機抽選！", "wrap": True, "flex": 5, "size": "sm", "color": "#666666" }
                    ]
                },
                {
                    "type": "box", "layout": "baseline", "margin": "md",
                    "contents": [
                        { "type": "text", "text": "說明", "color": "#AAAAAA", "size": "sm", "flex": 1 },
                        { "type": "text", "text": "「牛批貓+關鍵字」或「抽籤+關鍵字」將會從「關鍵字」對應的所有詞條中，隨機抽出一個回答。", "wrap": True, "flex": 5, "size": "sm", "color": "#666666" }
                    ]
                }
            ]
        },
        "footer": {
            "type": "box", "layout": "vertical",
            "contents": [
                { "type": "separator", "margin": "xxl" },
                {
                    "type": "button", "height": "sm", "style": "link",
                    "action": { "type": "message", "label": "範例步驟 1", "text": "學說話;抽神籤;甲子籤;乙丑籤;丙寅籤;丁卯籤;戊辰籤" }
                },
                {
                    "type": "button", "height": "sm", "style": "link",
                    "action": { "type": "message", "label": "範例步驟 2", "text": "抽籤抽神籤" }
                },
                {
                    "type": "button", "height": "sm", "style": "link",
                    "action": { "type": "message", "label": "主選單", "text": "主選單" }
                }
            ]
        }
    }

##聊天教學
def flexTeachChat(arg=[]):
    return {
        "type": "bubble", "direction": "ltr",
        "body": {
            "type": "box", "layout": "vertical",
            "contents": [
                # title
                { "type": "text", "text": "教學", "color": "#1DB446", "size": "sm", "weight": "bold" },
                { "type": "text", "text": "如何教我說話", "margin": "md", "size": "xxl", "weight": "bold" },
                { "type": "text", "text": "指令", "size": "md", "weight": "bold", "color": "#825d5c", "margin": "lg" },
                 # info
                {
                    "type": "box", "layout": "baseline", "margin": "md",
                    "contents": [
                        { "type": "text", "text": "學習詞條", "color": "#AAAAAA", "size": "sm", "flex": 1 },
                        { "type": "text", "text": "學說話;關鍵字;回答", "wrap": True, "flex": 3, "size": "sm", "color": "#825d5c" }
                    ]
                },
                {
                    "type": "box", "layout": "baseline", "margin": "md",
                    "contents": [
                        { "type": "text", "text": "大量學習", "color": "#AAAAAA", "size": "sm", "flex": 1 },
                        { "type": "text", "text": "學說話;關鍵字;回答1;回答N", "wrap": True, "flex": 3, "size": "sm", "color": "#825d5c" }
                    ]
                },
                {
                    "type": "box", "layout": "baseline", "margin": "md",
                    "contents": [
                        { "type": "text", "text": "刪除詞條", "color": "#AAAAAA", "size": "sm", "flex": 1 },
                        { "type": "text", "text": "忘記;關鍵字;回答", "wrap": True, "flex": 3, "size": "sm", "color": "#825d5c" }
                    ]
                },
                {
                    "type": "box", "layout": "baseline", "margin": "md",
                    "contents": [
                        { "type": "text", "text": "大量刪除", "color": "#AAAAAA", "size": "sm", "flex": 1 },
                        { "type": "text", "text": "忘記;關鍵字;回答1;回答N", "wrap": True, "flex": 3, "size": "sm", "color": "#825d5c" }
                    ]
                }
                ,
                {
                    "type": "box", "layout": "baseline", "margin": "md",
                    "contents": [
                        { "type": "text", "text": "降低詞條優先度", "color": "#AAAAAA", "size": "sm", "flex": 3 },
                        { "type": "text", "text": "壞壞", "wrap": True, "flex": 3, "size": "sm", "color": "#825d5c" }
                    ]
                }
            ]
        },
        "footer": {
            "type": "box", "layout": "vertical",
            "contents": [
                { "type": "separator", "margin": "xxl" },
                {
                    "type": "button", "style": "link", "height": "sm",
                    "action": { "type": "message", "label": "詞條學習範例", "text": "學說話;牛批牛批;本喵真牛批！" }
                },
                {
                    "type": "button", "style": "link", "height": "sm",
                    "action": { "type": "message", "label": "刪除詞條範例", "text": "忘記;牛批牛批;本喵真牛批！" }
                },
                {
                    "type": "button", "style": "link", "height": "sm",
                    "action": { "type": "message", "label": "牛批貓會說什麼", "text": "牛批貓會說什麼" }
                },
                {
                    "type": "button", "style": "link", "height": "sm",
                    "action": { "type": "message", "label": "主選單", "text": "主選單" }
                }
            ]
        }
    }

##查氣象教學
def flexTeachCWB(arg=[]):
    return {
        "type": "bubble", "direction": "ltr",
        "body": {
            "type": "box", "layout": "vertical",
            "contents": [
                # title
                { "type": "text", "text": "教學", "color": "#1DB446", "size": "sm", "weight": "bold" },
                { "type": "text", "text": "查氣象", "margin": "md", "size": "xxl", "weight": "bold" },
                # info
                {
                    "type": "box", "layout": "baseline", "margin": "md",
                    "contents": [
                        { "type": "text", "text": "空氣品質", "color": "#AAAAAA", "size": "sm", "flex": 3 },
                        { "type": "text", "text": "「測站名+空氣/空汙/空氣品質/PM2.5」", "wrap": True, "flex": 6, "size": "sm", "color": "#666666" }
                    ]
                },
                {
                    "type": "box", "layout": "baseline", "margin": "md",
                    "contents": [
                        { "type": "text", "text": "目前天氣", "color": "#AAAAAA", "size": "sm", "flex": 3 },
                        { "type": "text", "text": "「測站名+天氣/會下雨嗎」", "wrap": True, "flex": 6, "size": "sm", "color": "#666666" }
                    ]
                },
                {
                    "type": "box", "layout": "baseline", "margin": "md",
                    "contents": [
                        { "type": "text", "text": "一週天氣", "color": "#AAAAAA", "size": "sm", "flex": 3 },
                        { "type": "text", "text": "「縣市名+一週天氣/明天天氣/明天會下雨嗎」", "wrap": True, "flex": 6, "size": "sm", "color": "#666666" }
                    ]
                }
            ]
        },
        "footer": {
            "type": "box", "layout": "vertical",
            "contents": [
                { "type": "separator", "margin": "xxl" },
                {
                    "type": "button", "height": "sm", "style": "link",
                    "action": { "type": "message", "label": "查空氣範例", "text": "斗六空氣" }
                },
                {
                    "type": "button", "height": "sm", "style": "link",
                    "action": { "type": "message", "label": "查目前天氣範例", "text": "斗六天氣" }
                },
                {
                    "type": "button", "height": "sm", "style": "link",
                    "action": { "type": "message", "label": "查一週天氣範例", "text": "斗六一週天氣" }
                },
                {
                    "type": "button", "height": "sm", "style": "link",
                    "action": { "type": "message", "label": "主選單", "text": "主選單" }
                }
            ]
        }
    }

##教學選單
def flexTeaching(arg=[]):
    return {
        "type": "carousel",
        "contents": [
            flexTeachChat(),
            flexTeachLottery(),
            flexTeachCWB()
        ]
    }

##狀態選單
def flexStatusMenu(arg=[]):
    return {
        "type": "bubble", "direction": "ltr",
        "body": {
            "type": "box", "layout": "vertical",
            "contents": [
                { "type": "text", "text": "狀態", "size": "sm", "color": "#1DB446", "weight": "bold" },
                { "type": "text", "text": "目前狀態", "size": "xl", "weight": "bold", "margin": "md" },
                {
                    "type": "box", "layout": "vertical", "margin": "md",
                    "contents": [
                        {
                            "type": "box", "layout": "baseline",
                            "contents": [
                                { "type": "text", "text": "說話模式", "flex": 2, "color": "#AAAAAA" },
                                { "type": "text", "text": arg[0], "flex": 4, "color": "#666666", "wrap": True }
                            ]
                        },
                        {
                            "type": "box", "layout": "baseline",
                            "contents": [
                                { "type": "text", "text": "目前狀態", "flex": 2, "color": "#AAAAAA" },
                                { "type": "text", "text": arg[1], "flex": 4, "color": "#666666", "wrap": True }
                            ]
                        }
                    ]
                }
            ]
        },
        "footer": {
            "type": "box", "layout": "vertical",
            "contents": [
                { "type": "separator" },
                {
                    "type": "button", "height": "sm", "style": "link",
                    "action": { "type": "message", "label": "切換說話模式", "text": '不可以說別人教的話' if arg[2] else '可以說別人教的話' }
                },
                {
                    "type": "button", "height": "sm", "style": "link",
                    "action": { "type": "message", "label": "切換目前狀態", "text": '牛批貓講話' if arg[3] else '牛批貓安靜' }
                },
                {
                    "type": "button", "height": "sm", "style": "link",
                    "action": { "type": "message", "label": "主選單", "text": "主選單" }
                }
            ]
        }
    }

##會說什麼
def flexWhatCanSay(arg=[]):
    #整理資料格式
    keywordObj=[]
    if arg[5]!="Null":
        for k, v in arg[5].items():
            if len(keywordObj): keywordObj.append({ "type": "separator", "margin": "md" })
            keywordObj.append(
                {
                    "type": "box", "layout": "horizontal", "margin": "md",
                    "contents": [
                        { "type": "text", "text": k, "size": "sm", "color": "#690808", "weight": "bold", "wrap": True, "flex": 1 },
                        {
                            "type": "box", "layout": "vertical",
                            "contents": [
                                { "type": "text", "text": s, "size": "sm", "color": "#111111", "align": "end", "wrap": True } for s in v
                            ]
                        }
                    ]
                }
            )
    if not len(keywordObj): keywordObj.append({ "type": "filler" })
    #建立容器
    return {
        "type": "bubble", "direction": "ltr",
        "body": {
            "type": "box", "layout": "vertical",
            "contents": [
                { "type": "text", "text": "詞條", "size": "sm", "color": "#1DB446", "weight": "bold" },
                { "type": "text", "text": "這裡教我說的話", "margin": "md", "size": "xl", "weight": "bold" },
                { "type": "text", "text": '說話模式：'+arg[0], "size": "xs", "color": "#AAAAAA" },
                { "type": "text", "text": '目前狀態：'+arg[1], "size": "xs", "color": "#AAAAAA" },
                { "type": "separator", "margin": "md" },
                {
                    "type": "box", "layout": "vertical", "margin": "md",
                    "contents": [x for x in keywordObj]
                },
                { "type": "separator", "margin": "md" },
                {
                    "type": "box", "layout": "horizontal", "margin": "md",
                    "contents": [
                        { "type": "text", "text": "關鍵字數量", "size": "sm", "color": "#aaaaaa" },
                        { "type": "text", "text": str(arg[2]), "size": "sm", "color": "#aaaaaa", "align": "end" }
                    ]
                },
                {
                    "type": "box", "layout": "horizontal", "margin": "md",
                    "contents": [
                        { "type": "text", "text": "詞條數量", "size": "sm", "color": "#aaaaaa" },
                        { "type": "text", "text": str(arg[3]), "size": "sm", "color": "#aaaaaa", "align": "end" }
                    ]
                },
                { "type": "separator", "margin": "md" },
                { "type": "text", "text": '截至'+arg[4], "size": "xs", "color": "#aaaaaa", "margin": "md", "align": "end" }
            ]
        }
    }

##空氣品質
def flexAQI(arg={}):
    #整理資料格式
    arg['SiteName'] = arg['SiteName'][arg['SiteName'].index('(')+1:arg['SiteName'].index(')')] if '(' in arg['SiteName'] else arg['SiteName']
    arg['AQI'] = '-1' if arg['AQI']=='' else arg['AQI']
    for x in ['SO2', 'SO2_AVG', 'CO', 'CO_8hr', 'O3', 'O3_8hr', 'PM10', 'PM10_AVG', 'PM2.5', 'PM2.5_AVG', 'NO2']:
        arg[x] = 'NA' if arg[x]=='' else arg[x]
    AQIList = [[-1,"#888888"], [0,"#339933"], [51,"#EECC33"], [101,"#EE9933"], [151,"#DD3333"], [201,"#996699"], [301,"#990066"]]
    AQIcolor = list(filter(lambda x: int(arg['AQI'])>=x[0], AQIList))[::-1][0][1]
    #建立容器
    return {
        "type": "bubble", "direction": "ltr",
        "body": {
            "type": "box", "layout": "vertical",
            "contents": [
                # title
                { "type": "text", "text": arg['Status'], "weight": "bold", "size": "sm", "color": AQIcolor },
                {
                    "type": "box", "layout": "horizontal", "margin": "md",
                    "contents": [
                        {
                            "type": "box", "layout": "vertical", "flex": 5,
                            "contents": [
                                { "type": "text", "text": arg['SiteName'], "size": "xxl", "weight": "bold" },
                                { "type": "text", "text": arg['County'], "size": "lg", "weight": "bold", "color": "#333399" }
                            ]
                        },
                        {
                            "type": "box", "layout": "vertical", "flex": 3,
                            "contents": [
                                { "type": "text", "text": "AQI", "size": "lg", "align": "end", "color": AQIcolor  },
                                { "type": "text", "text": arg['AQI'] if arg['AQI']!='-1' else 'NA', "size": "4xl", "weight": "bold", "color": AQIcolor, "align": "end" }
                            ]
                        }
                    ]
                },
                { "type": "separator", "margin": "md" },
                # O3 臭氧
                {
                    "type": "box", "layout": "horizontal", "margin": "md",
                    "contents": [
                        {
                            "type": "box", "layout": "vertical", "flex": 3,
                            "contents": [ { "type": "text", "text": "O3\n臭氧", "weight": "bold", "size": "lg", "wrap": True, "flex": 1, "align": "start", "color": "#336699" if "臭氧" in arg['Pollutant'] else "#444444", "gravity": "center" } ]
                        },
                        {
                            "type": "box", "layout": "vertical", "flex": 2,
                            "contents": [
                                { "type": "text", "text": "8小時\n移動平均", "size": "sm", "wrap": True, "flex": 1, "align": "end", "gravity": "center" },
                                { "type": "text", "text": "小時濃度", "size": "sm", "wrap": True, "flex": 1, "align": "end", "gravity": "center" }
                            ]
                        },
                        {
                            "type": "box", "layout": "vertical", "flex": 2,
                            "contents": [
                                { "type": "text", "text": arg['O3_8hr'], "size": "xxl", "wrap": True, "flex": 1, "align": "end", "gravity": "center", "weight": "bold" },
                                { "type": "text", "text": arg['O3'], "size": "xxl", "wrap": True, "flex": 1, "align": "end", "gravity": "center", "weight": "bold" }
                            ]
                        }
                    ]
                },
                { "type": "separator", "margin": "md" },
                # PM2.5 細懸浮微粒
                {
                    "type": "box", "layout": "horizontal", "margin": "md",
                    "contents": [
                        {
                            "type": "box", "layout": "vertical", "flex": 3,
                            "contents": [ { "type": "text", "text": "PM2.5\n細懸浮微粒", "weight": "bold", "size": "lg", "wrap": True, "flex": 1, "align": "start", "color": "#336699" if "細懸浮微粒" in arg['Pollutant'] else "#444444", "gravity": "center" } ]
                        },
                        {
                            "type": "box", "layout": "vertical", "flex": 2,
                            "contents": [
                                { "type": "text", "text": "移動平均", "size": "sm", "wrap": True, "flex": 1, "align": "end", "gravity": "center" },
                                { "type": "text", "text": "小時濃度", "size": "sm", "wrap": True, "flex": 1, "align": "end", "gravity": "center" }
                            ]
                        },
                        {
                            "type": "box", "layout": "vertical", "flex": 2,
                            "contents": [
                                { "type": "text", "text": arg['PM2.5_AVG'], "size": "xxl", "wrap": True, "flex": 1, "align": "end", "gravity": "center", "weight": "bold" },
                                { "type": "text", "text": arg['PM2.5'], "size": "xxl", "wrap": True, "flex": 1, "align": "end", "gravity": "center", "weight": "bold" }
                            ]
                        }
                    ]
                },
                { "type": "separator", "margin": "md" },
                # PM10 懸浮微粒
                {
                    "type": "box", "layout": "horizontal", "margin": "md",
                    "contents": [
                        {
                            "type": "box", "layout": "vertical", "flex": 3,
                            "contents": [ { "type": "text", "text": "PM10\n懸浮微粒", "weight": "bold", "size": "lg", "wrap": True, "flex": 1, "align": "start", "color": "#336699" if "懸浮微粒" in arg['Pollutant'].replace("細懸浮微粒","") else "#444444", "gravity": "center" } ]
                        },
                        {
                            "type": "box", "layout": "vertical", "flex": 2,
                            "contents": [
                                { "type": "text", "text": "移動平均", "size": "sm", "wrap": True, "flex": 1, "align": "end", "gravity": "center" },
                                { "type": "text", "text": "小時濃度", "size": "sm", "wrap": True, "flex": 1, "align": "end", "gravity": "center" }
                            ]
                        },
                        {
                            "type": "box", "layout": "vertical", "flex": 2,
                            "contents": [
                                { "type": "text", "text": arg['PM10_AVG'], "size": "xxl", "wrap": True, "flex": 1, "align": "end", "gravity": "center", "weight": "bold" },
                                { "type": "text", "text": arg['PM10'], "size": "xxl", "wrap": True, "flex": 1, "align": "end", "gravity": "center", "weight": "bold" }
                            ]
                        }
                    ]
                },
                { "type": "separator", "margin": "md" },
                # CO 一氧化碳
                {
                    "type": "box", "layout": "horizontal", "margin": "md",
                    "contents": [
                        {
                            "type": "box", "layout": "vertical", "flex": 3,
                            "contents": [ { "type": "text", "text": "CO\n一氧化碳", "weight": "bold", "size": "lg", "wrap": True, "flex": 1, "align": "start", "color": "#336699" if "一氧化碳" in arg['Pollutant'] else "#444444", "gravity": "center" } ]
                        },
                        {
                            "type": "box", "layout": "vertical", "flex": 2,
                            "contents": [
                                { "type": "text", "text": "8小時\n移動平均", "size": "sm", "wrap": True, "flex": 1, "align": "end", "gravity": "center" },
                                { "type": "text", "text": "小時濃度", "size": "sm", "wrap": True, "flex": 1, "align": "end", "gravity": "center" }
                            ]
                        },
                        {
                            "type": "box", "layout": "vertical", "flex": 2,
                            "contents": [
                                { "type": "text", "text": arg['CO_8hr'], "size": "xxl", "wrap": True, "flex": 1, "align": "end", "gravity": "center", "weight": "bold" },
                                { "type": "text", "text": arg['CO'], "size": "xxl", "wrap": True, "flex": 1, "align": "end", "gravity": "center", "weight": "bold" }
                            ]
                        }
                    ]
                },
                { "type": "separator", "margin": "md" },
                # SO2 二氧化硫
                {
                    "type": "box", "layout": "horizontal", "margin": "md",
                    "contents": [
                        {
                            "type": "box", "layout": "vertical", "flex": 3,
                            "contents": [ { "type": "text", "text": "SO2\n二氧化硫", "weight": "bold", "size": "lg", "wrap": True, "flex": 1, "align": "start", "color": "#336699" if "二氧化硫" in arg['Pollutant'] else "#444444", "gravity": "center" } ]
                        },
                        {
                            "type": "box", "layout": "vertical", "flex": 2,
                            "contents": [
                                { "type": "text", "text": "移動平均", "size": "sm", "wrap": True, "flex": 1, "align": "end", "gravity": "center" },
                                { "type": "text", "text": "小時濃度", "size": "sm", "wrap": True, "flex": 1, "align": "end", "gravity": "center" }
                            ]
                        },
                        {
                            "type": "box", "layout": "vertical", "flex": 2,
                            "contents": [
                                { "type": "text", "text": arg['SO2_AVG'], "size": "xxl", "wrap": True, "flex": 1, "align": "end", "gravity": "center", "weight": "bold" },
                                { "type": "text", "text": arg['SO2'], "size": "xxl", "wrap": True, "flex": 1, "align": "end", "gravity": "center", "weight": "bold" }
                            ]
                        }
                    ]
                },
                { "type": "separator", "margin": "md" },
                # NO2 二氧化氮
                {
                    "type": "box", "layout": "horizontal", "margin": "md",
                    "contents": [
                        {
                            "type": "box", "layout": "vertical", "flex": 3,
                            "contents": [ { "type": "text", "text": "NO2\n二氧化氮", "weight": "bold", "size": "lg", "wrap": True, "flex": 1, "align": "start", "color": "#336699" if "二氧化氮" in arg['Pollutant'] else "#444444", "gravity": "center" } ]
                        },
                        {
                            "type": "box", "layout": "vertical", "flex": 2,
                            "contents": [ { "type": "text", "text": "小時濃度", "size": "sm", "wrap": True, "flex": 1, "align": "end", "gravity": "center" } ]
                        },
                        {
                            "type": "box", "layout": "vertical", "flex": 2,
                            "contents": [ { "type": "text", "text": arg['NO2'], "size": "xxl", "wrap": True, "flex": 1, "align": "end", "gravity": "center", "weight": "bold" } ]
                        }
                    ]
                },
                { "type": "separator", "margin": "md" },
                { "type": "text", "text": '截至'+arg['timeStr'], "margin": "xs", "size": "xs", "color": "#aaaaaa", "align": "end" }
            ]
        }
    }

##目前天氣
def flexWeather(arg={}):
    #整理資料格式
    arg['Temp'] = str(round(float(arg['Temp'])*10+0.5)/10) if arg['Temp']!='-99' else 'N/A'
    arg['Humd'] = str(round(float(arg['Humd'])*1000+0.5)/10) if arg['Humd']!='-99' else 'N/A'
    arg['24R'] = str(round(float(arg['24R'])*10+0.5)/10) if arg['24R']!='-99' else 'N/A'
    #建立容器
    return {
        "type": "bubble", "direction": "ltr",
        "body": {
            "type": "box", "layout": "vertical",
            "contents": [
                #溫度
                { "type": "text", "text": arg['Temp']+'°', "color": "#990066", "size": "5xl", "align": "center" },
                { "type": "text", "text": arg['Wx'], "color": "#990066", "size": "lg", "weight": "bold", "align": "center" },
                #目前天氣
                {
                    "type": "box", "layout": "horizontal", "margin": "xxl",
                    "contents": [
                        #地區
                        {
                            "type": "box", "layout": "vertical", "flex": 5,
                            "contents": [
                                { "type": "text", "text": arg['locationName'], "size": "xxl", "weight": "bold", "wrap": True },
                                { "type": "text", "text": arg['City']+' '+arg['Town'], "weight": "bold", "size": "sm", "color": "#0D8186" }
                            ]
                        },
                        #降雨率
                        {
                            "type": "box", "layout": "vertical", "flex": 4,
                            "contents": [
                                {
                                    "type": "box", "layout": "baseline",
                                    "contents": [
                                        { "type": "text", "text": "降雨率", "flex": 2, "size": "sm", "weight": "bold" },
                                        { "type": "text", "text": str(arg['PoP6h'])+'%', "flex": 3, "weight": "bold", "size": "xl", "color": "#0D8186" }
                                    ]
                                },
                                {
                                    "type": "box", "layout": "vertical", "height": "15px", "margin": "sm",
                                    "backgroundColor": "#9FD8E3", "cornerRadius": "10px",
                                    "contents": [
                                        {
                                            "type": "box", "layout": "vertical", "height": "15px",
                                            "backgroundColor": "#0D8186", "width": str(arg['PoP6h'])+'%', "cornerRadius": "10px",
                                            "contents": [ { "type": "filler" } ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                { "type": "separator", "margin": "md" },
                #濕度、雨量
                {
                    "type": "box", "layout": "horizontal", "margin": "md",
                    "contents": [
                        {
                            "type": "box", "layout": "vertical",
                            "contents": [
                                { "type": "text", "text": "濕度", "size": "sm", "align": "center" },
                                { "type": "text", "text": arg['Humd']+'%', "weight": "bold", "size": "lg", "color": "#990066", "align": "center" }
                            ]
                        },
                        {
                            "type": "box", "layout": "vertical",
                            "contents": [
                                { "type": "text", "text": "日積雨量", "size": "sm", "align": "center" },
                                { "type": "text", "text": arg['24R']+' mm', "weight": "bold", "size": "lg", "color": "#990066", "align": "center" }
                            ]
                        }
                    ]
                },
                { "type": "separator", "margin": "md" },
                {
                    "type": "box", "layout": "vertical", "margin": "md",
                    "contents": [ { "type": "text", "text": '截至'+arg['TimeString'], "size": "sm", "color": "#AAAAAA", "align": "end" } ]
                }
            ]
        }
    }

##未來天氣
def flexWeather72HR(arg):
    #整理資料格式
    WeatherList=[]
    for x in arg:
        WeatherList.append(
            {
                "type": "bubble", "size": "micro", "direction": "ltr",
                "body": {
                    "type": "box", "layout": "vertical",
                    "contents": [
                        #Title
                        {
                            "type": "box", "layout": "horizontal",
                            "contents": [
                                { "type": "text", "text": x['locationName'], "size": "sm", "align": "center", "flex": 4, "color": "#0D8186" },
                                { "type": "text", "text": x['startTime'][8:14]+'時', "color": "#1DB446", "size": "xs", "align": "center", "flex": 5 }
                            ]
                        },
                        #天氣內容
                        { "type": "text", "text": x['Temp']+'°', "size": "3xl", "color": "#990066", "align": "center" },
                        { "type": "text", "text": x['Wx'], "size": "sm", "weight": "bold", "align": "center", "color": "#990066" },
                        { "type": "separator", "margin": "md" },
                        {
                            "type": "box", "layout": "horizontal", "margin": "md",
                            "contents": [
                                {
                                    "type": "box", "layout": "vertical", "flex": 5,
                                    "contents": [
                                        { "type": "text", "text": "降雨率", "size": "xs", "color": "#666666", "align": "center" },
                                        { "type": "text", "text": x['PoP6h']+'%', "size": "md", "weight": "bold", "color": "#0D8186", "align": "center" }
                                    ]
                                },
                                { "type": "separator", "margin": "md" },
                                {
                                    "type": "box", "layout": "vertical", "flex": 5,
                                    "contents": [
                                        { "type": "text", "text": "舒適度", "size": "xs", "color": "#666666", "align": "center" },
                                        { "type": "text", "text": x['CI'], "size": "md", "weight": "bold", "color": "#0D8186", "align": "center" }
                                    ]
                                }
                            ]
                        },
                        { "type": "separator", "margin": "md" }
                    ]
                }
            }
        )
    
    #建立容器
    return { "type": "carousel", "contents": WeatherList }

##擲筊
def flexDevinate(arg):
    img = [
        'https://i.imgur.com/D0GE3Vf.png', 'https://i.imgur.com/cm5pdAg.png',
        'https://i.imgur.com/cm5pdAg.png', 'https://i.imgur.com/1tYF5LW.png'
    ]
    res = ['笑筊', '聖筊', '聖筊', '陰筊']
    return {
        "type": "bubble",
        "size": "kilo",
        "direction": "ltr",
        "hero": {
            "type": "image",
            "url": img[arg],
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "20:13"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#c4241b",
            "contents": [
                {
                    "type": "text",
                    "text": res[arg],
                    "size": "4xl",
                    "color": "#ffffff",
                    "weight": "bold",
                    "align": "center"
                },
                {
                    "type": "separator",
                    "color": "#ffffff",
                    "margin": "md"
                },
                {
                    "type": "button",
                    "style": "link",
                    "color": "#ffffff",
                    "action": {
                        "type": "message",
                        "label": "再擲一次",
                        "text": "擲筊"
                    }
                }
            ]
        }
    }

