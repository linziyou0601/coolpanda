from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

##主選單
def mainMenu(arg=[]):
    return BubbleContainer(
                direction='ltr',
                hero=ImageComponent(
                    url='https://i.imgur.com/kW0Fr2H.png',
                    size='full',
                    aspect_ratio='20:13',
                    aspect_mode='cover'
                ),
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        # title
                        TextComponent(text='牛批熊貓', weight='bold', size='xl'),
                        # info
                        BoxComponent(
                            layout='vertical',
                            margin='lg',
                            spacing='sm',
                            contents=[
                                BoxComponent(
                                    layout='baseline',
                                    spacing='sm',
                                    contents=[
                                        TextComponent(
                                            text='功能',
                                            color='#aaaaaa',
                                            size='sm',
                                            flex=2
                                        ),
                                        TextComponent(
                                            text='胡言亂語、抽籤、查時間',
                                            wrap=True,
                                            color='#666666',
                                            size='sm',
                                            flex=4
                                        )
                                    ],
                                ),
                                BoxComponent(
                                    layout='baseline',
                                    spacing='sm',
                                    contents=[
                                        TextComponent(
                                            text='維護時間',
                                            color='#aaaaaa',
                                            size='sm',
                                            flex=2
                                        ),
                                        TextComponent(
                                            text="我爽就維護(◕ܫ◕)",
                                            wrap=True,
                                            color='#666666',
                                            size='sm',
                                            flex=4,
                                        )
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                footer=BoxComponent(
                    layout='vertical',
                    spacing='sm',
                    contents=[
                        ButtonComponent(
                            style='link',
                            height='sm',
                            action=MessageAction(
                                label='功能教學',
                                text='牛批貓會幹嘛'
                            ),
                        ),
                        ButtonComponent(
                            style='link',
                            height='sm',
                            action=MessageAction(
                                label='目前狀態',
                                text='目前狀態'
                            ),
                        ),
                        SpacerComponent(size='sm')
                    ],
                    flex=0
                ),
            )

##抽籤教學
def teachLottery(arg=[]):
    return BubbleContainer(
                direction='ltr',
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        # title
                        TextComponent(text='教學', weight='bold', size='sm', color="#1DB446"),
                        TextComponent(text='抽籤教學', weight='bold', size='xxl', margin='md'),
                        # info
                        BoxComponent(
                            layout='vertical',
                            margin='lg',
                            spacing='sm',
                            contents=[
                                BoxComponent(
                                    layout='baseline',
                                    spacing='sm',
                                    contents=[
                                        TextComponent(
                                            text='注意',
                                            color='#aaaaaa',
                                            size='sm',
                                            flex=1
                                        ),
                                        TextComponent(
                                            text='若有開啟「可以說別人教的話」的功能，則也會從其他聊天室教的詞條隨機抽選！',
                                            wrap=True,
                                            color='#666666',
                                            size='sm',
                                            flex=5
                                        )
                                    ],
                                ),
                                BoxComponent(
                                    layout='baseline',
                                    spacing='sm',
                                    contents=[
                                        TextComponent(
                                            text='說明',
                                            color='#aaaaaa',
                                            size='sm',
                                            flex=1
                                        ),
                                        TextComponent(
                                            text='「牛批貓關鍵字」或「抽籤關鍵字」將會從「關鍵字」對應的所有詞條中，隨機抽出一個回答。',
                                            wrap=True,
                                            color='#666666',
                                            size='sm',
                                            flex=5
                                        )
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                footer=BoxComponent(
                    layout='vertical',
                    spacing='sm',
                    contents=[
                        SeparatorComponent(margin='xxl'),
                        ButtonComponent(
                            style='link',
                            height='sm',
                            action=MessageAction(
                                label='① 加入籤',
                                text='學說話;抽神籤;甲子籤;乙丑籤;丙寅籤;丁卯籤;戊辰籤'
                            ),
                        ),
                        ButtonComponent(
                            style='link',
                            height='sm',
                            action=MessageAction(
                                label='② 抽一支籤',
                                text='抽籤抽神籤'
                            ),
                        ),
                        ButtonComponent(
                            style='link',
                            height='sm',
                            action=MessageAction(
                                label='主選單',
                                text='主選單'
                            ),
                        ),
                        SpacerComponent(size='sm')
                    ],
                    flex=0,
                ),
            )

##聊天教學
def teachChat(arg=[]):
    return BubbleContainer(
                direction='ltr',
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        # title
                        TextComponent(text='教學', weight='bold', size='sm', color="#1DB446"),
                        TextComponent(text='如何教我說話', weight='bold', size='xxl', margin='md'),
                        TextComponent(text='指令', weight='bold', color='#825d5c', margin='lg', size='md'),
                        # info
                        BoxComponent(
                            layout='vertical',
                            margin='md',
                            spacing='sm',
                            contents=[
                                BoxComponent(
                                    layout='baseline',
                                    spacing='sm',
                                    contents=[
                                        TextComponent(
                                            text='學習詞條',
                                            color='#aaaaaa',
                                            size='sm',
                                            flex=1
                                        ),
                                        TextComponent(
                                            text='學說話;關鍵字;回答',
                                            wrap=True,
                                            color='#825d5c',
                                            size='sm',
                                            flex=3
                                        )
                                    ],
                                ),
                                BoxComponent(
                                    layout='baseline',
                                    spacing='sm',
                                    contents=[
                                        TextComponent(
                                            text='大量學習',
                                            color='#aaaaaa',
                                            size='sm',
                                            flex=1
                                        ),
                                        TextComponent(
                                            text='學說話;關鍵字;回答1;回答N',
                                            wrap=True,
                                            color='#825d5c',
                                            size='sm',
                                            flex=3
                                        )
                                    ],
                                ),
                                BoxComponent(
                                    layout='baseline',
                                    spacing='sm',
                                    contents=[
                                        TextComponent(
                                            text='刪除詞條',
                                            color='#aaaaaa',
                                            size='sm',
                                            flex=1
                                        ),
                                        TextComponent(
                                            text='忘記;關鍵字;回答',
                                            wrap=True,
                                            color='#825d5c',
                                            size='sm',
                                            flex=3
                                        )
                                    ],
                                ),BoxComponent(
                                    layout='baseline',
                                    spacing='sm',
                                    contents=[
                                        TextComponent(
                                            text='大量刪除',
                                            color='#aaaaaa',
                                            size='sm',
                                            flex=1
                                        ),
                                        TextComponent(
                                            text='忘記;關鍵字;回答1;回答N',
                                            wrap=True,
                                            color='#825d5c',
                                            size='sm',
                                            flex=3
                                        )
                                    ],
                                ),BoxComponent(
                                    layout='baseline',
                                    spacing='sm',
                                    contents=[
                                        TextComponent(
                                            text='降低詞條優先度',
                                            color='#aaaaaa',
                                            size='sm',
                                            flex=3
                                        ),
                                        TextComponent(
                                            text='壞壞',
                                            wrap=True,
                                            color='#825d5c',
                                            size='sm',
                                            flex=3
                                        )
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                footer=BoxComponent(
                    layout='vertical',
                    spacing='sm',
                    contents=[
                        SeparatorComponent(margin='xxl'),
                        ButtonComponent(
                            style='link',
                            height='sm',
                            action=MessageAction(
                                label='詞條學習範例',
                                text='學說話;牛批牛批;本喵真牛批！'
                            ),
                        ),
                        ButtonComponent(
                            style='link',
                            height='sm',
                            action=MessageAction(
                                label='刪除詞條範例',
                                text='忘記;牛批牛批;本喵真牛批！'
                            ),
                        ),
                        ButtonComponent(
                            style='link',
                            height='sm',
                            action=MessageAction(
                                label='你會說什麼',
                                text='牛批貓會說什麼'
                            ),
                        ),
                        ButtonComponent(
                            style='link',
                            height='sm',
                            action=MessageAction(
                                label='主選單',
                                text='主選單'
                            ),
                        )
                    ],
                    flex=0
                ),
            )

##查時間教學
def teachDatetime(arg=[]):
    return BubbleContainer(
                direction='ltr',
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        # title
                        TextComponent(text='教學', weight='bold', size='sm', color="#1DB446"),
                        TextComponent(text='時間和日期', weight='bold', size='xxl', margin='md'),
                        TextComponent(text='指令', weight='bold', color='#825d5c', margin='lg', size='md'),
                        # info
                        BoxComponent(
                            layout='vertical',
                            margin='md',
                            spacing='sm',
                            contents=[
                                BoxComponent(
                                    layout='baseline',
                                    spacing='sm',
                                    contents=[
                                        TextComponent(
                                            text='查時間',
                                            color='#aaaaaa',
                                            size='sm',
                                            flex=1
                                        ),
                                        TextComponent(
                                            text='現在時間、現在幾點',
                                            wrap=True,
                                            color='#825d5c',
                                            size='sm',
                                            flex=3
                                        )
                                    ],
                                ),
                                BoxComponent(
                                    layout='baseline',
                                    spacing='sm',
                                    contents=[
                                        TextComponent(
                                            text='查日期',
                                            color='#aaaaaa',
                                            size='sm',
                                            flex=1
                                        ),
                                        TextComponent(
                                            text='今天、明天、後天、幾月幾號...',
                                            wrap=True,
                                            color='#825d5c',
                                            size='sm',
                                            flex=3
                                        )
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                footer=BoxComponent(
                    layout='vertical',
                    spacing='sm',
                    contents=[
                        SeparatorComponent(margin='xxl'),
                        ButtonComponent(
                            style='link',
                            height='sm',
                            action=MessageAction(
                                label='查時間範例',
                                text='現在幾點'
                            ),
                        ),
                        ButtonComponent(
                            style='link',
                            height='sm',
                            action=MessageAction(
                                label='查日期範例',
                                text='今天幾號'
                            ),
                        ),
                        ButtonComponent(
                            style='link',
                            height='sm',
                            action=MessageAction(
                                label='主選單',
                                text='主選單'
                            ),
                        )
                    ],
                    flex=0
                ),
            )

##查空氣教學
def teachAQI(arg=[]):
    return BubbleContainer(
                direction='ltr',
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        # title
                        TextComponent(text='教學', weight='bold', size='sm', color="#1DB446"),
                        TextComponent(text='查空氣品質', weight='bold', size='xxl', margin='md'),
                        # info
                        BoxComponent(
                            layout='vertical',
                            margin='md',
                            spacing='sm',
                            contents=[
                                BoxComponent(
                                    layout='baseline',
                                    spacing='sm',
                                    contents=[
                                        TextComponent(
                                            text='關鍵字',
                                            color='#aaaaaa',
                                            size='sm',
                                            flex=1
                                        ),
                                        TextComponent(
                                            text='「測站名+空氣/空汙/空氣品質/PM2.5」的方式，結尾若為關鍵字，則會將關鍵字前的詞帶入查詢',
                                            wrap=True,
                                            color='#666666',
                                            size='sm',
                                            flex=5
                                        )
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                footer=BoxComponent(
                    layout='vertical',
                    spacing='sm',
                    contents=[
                        SeparatorComponent(margin='xxl'),
                        ButtonComponent(
                            style='link',
                            height='sm',
                            action=MessageAction(
                                label='查空氣範例',
                                text='斗六空氣'
                            ),
                        ),
                        ButtonComponent(
                            style='link',
                            height='sm',
                            action=MessageAction(
                                label='主選單',
                                text='主選單'
                            ),
                        )
                    ],
                    flex=0
                ),
            )

##教學選單
def teaching(arg=[]):
    return CarouselContainer(
        contents=[
            teachChat(),
            teachLottery(),
            teachAQI(),
            teachDatetime()
        ]
    )

##狀態選單
def statusMenu(arg=[]):
    return BubbleContainer(
                direction='ltr',
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        # title
                        TextComponent(text='狀態', weight='bold', size='sm', color="#1DB446"),
                        TextComponent(text='目前狀態', weight='bold', size='xxl', margin='md'),
                        # info
                        BoxComponent(
                            layout='vertical',
                            margin='lg',
                            spacing='sm',
                            contents=[
                                BoxComponent(
                                    layout='baseline',
                                    spacing='sm',
                                    contents=[
                                        TextComponent(
                                            text='說話模式',
                                            color='#aaaaaa',
                                            size='sm',
                                            flex=2
                                        ),
                                        TextComponent(
                                            text=arg[0],
                                            wrap=True,
                                            color='#666666',
                                            size='sm',
                                            flex=4
                                        )
                                    ],
                                ),
                                BoxComponent(
                                    layout='baseline',
                                    spacing='sm',
                                    contents=[
                                        TextComponent(
                                            text='目前狀態',
                                            color='#aaaaaa',
                                            size='sm',
                                            flex=2
                                        ),
                                        TextComponent(
                                            text=arg[1],
                                            wrap=True,
                                            color='#666666',
                                            size='sm',
                                            flex=4
                                        )
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                footer=BoxComponent(
                    layout='vertical',
                    spacing='sm',
                    contents=[
                        SeparatorComponent(margin='xxl'),
                        ButtonComponent(
                            style='link',
                            height='sm',
                            action=MessageAction(
                                label='切換說話模式',
                                text='不可以說別人教的話' if arg[2] else '可以說別人教的話'
                            ),
                        ),
                        ButtonComponent(
                            style='link',
                            height='sm',
                            action=MessageAction(
                                label='切換目前狀態',
                                text='牛批貓講話' if arg[3] else '牛批貓安靜'
                            ),
                        ),
                        ButtonComponent(
                            style='link',
                            height='sm',
                            action=MessageAction(
                                label='主選單',
                                text='主選單'
                            ),
                        ),
                        SpacerComponent(size='sm')
                    ],
                    flex=0
                ),
            )

##會說什麼
def whatCanSay(arg=[]):
    keywordObj=[]
    if arg[5]!="Null":
        for k, v in arg[5].items():
            keywordObj.append(
                BoxComponent(
                    layout='horizontal', margin='md',
                    contents=[
                        TextComponent(text=k, weight='bold', color='#690808', size='sm', wrap=True, flex=1),
                        BoxComponent(
                            layout='vertical',
                            contents=[
                                TextComponent(text=s, color='#111111', size='sm', align='end', wrap=True) for s in v
                            ],
                        )
                    ],
                )
            )
            keywordObj.append(SeparatorComponent(margin='md'))
    if not len(keywordObj): keywordObj.append(SeparatorComponent(margin='md'))
    return BubbleContainer(
                direction='ltr',
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        # title
                        TextComponent(text='詞條', weight='bold', size='sm', color="#1DB446"),
                        TextComponent(text='這裡教我說的話', weight='bold', size='xl', margin='md'),
                        TextComponent(text='說話模式：'+arg[0], color='#aaaaaa', size='xs'),
                        TextComponent(text='目前狀態：'+arg[1], color='#aaaaaa', size='xs'),
                        SeparatorComponent(margin='md'),
                        BoxComponent(
                            layout='vertical',
                            margin='md',
                            spacing='sm',
                            contents=[x for x in keywordObj],
                        ),
                        # info
                        BoxComponent(
                            layout='horizontal',
                            margin='md',
                            contents=[
                                TextComponent(
                                    text='關鍵字數量',
                                    color='#aaaaaa',
                                    size='sm',
                                ),
                                TextComponent(
                                    text=str(arg[2]),
                                    color='#aaaaaa',
                                    size='sm',
                                    align='end'
                                )
                            ],
                        ),
                        BoxComponent(
                            layout='horizontal',
                            margin='md',
                            contents=[
                                TextComponent(
                                    text='詞條數量',
                                    color='#aaaaaa',
                                    size='sm',
                                ),
                                TextComponent(
                                    text=str(arg[3]),
                                    color='#aaaaaa',
                                    size='sm',
                                    align='end'
                                )
                            ],
                        ),
                        BoxComponent(
                            layout='vertical',
                            margin='xs',
                            contents=[
                                TextComponent(
                                    text='截至'+arg[4],
                                    color='#aaaaaa',
                                    size='xs',
                                    align='end'
                                )
                            ],
                        )
                    ],
                ),
            )

##空氣品質
def nowAQI(arg={}):
    arg['SiteName'] = arg['SiteName'][arg['SiteName'].index('(')+1:arg['SiteName'].index(')')] if '(' in arg['SiteName'] else arg['SiteName']
    arg['AQI'] = '-1' if arg['AQI']=='' else arg['AQI']
    for x in ['SO2', 'SO2_AVG', 'CO', 'CO_8hr', 'O3', 'O3_8hr', 'PM10', 'PM10_AVG', 'PM2.5', 'PM2.5_AVG', 'NO2']:
        arg[x] = 'NA' if arg[x]=='' else arg[x]
    AQIList = [[-1,"#888888"], [0,"#339933"], [51,"#EECC33"], [101,"#EE9933"], [151,"#DD3333"], [201,"#996699"], [301,"#990066"]]
    AQIcolor = list(filter(lambda x: int(arg['AQI'])>=x[0], AQIList))[::-1][0][1]
    return BubbleContainer(
                direction='ltr',
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        # title
                        TextComponent(text='空氣品質', weight='bold', size='sm', color="#1DB446"),
                        BoxComponent(
                            layout='horizontal',
                            margin='md',
                            contents=[
                                BoxComponent(
                                    layout='vertical', flex=5,
                                    contents=[
                                        TextComponent(text=arg['SiteName'], weight='bold', size='xxl'),
                                        TextComponent(text=arg['County'], weight='bold', size='md', color="#333399")
                                    ],
                                ),
                                BoxComponent(
                                    layout='vertical', flex=3,
                                    contents=[
                                        TextComponent(text='AQI ' + arg['AQI'], weight='bold', size='xl', color=AQIcolor, align="end"),
                                        TextComponent(text=arg['Status'], weight='bold', size='xl', color=AQIcolor, align="end")
                                    ],
                                ),
                            ],
                        ),
                        # O3 臭氧
                        SeparatorComponent(margin='md'),
                        BoxComponent(
                            layout='horizontal',
                            margin='md',
                            contents=[
                                BoxComponent(
                                    layout='vertical', flex=3,
                                    contents=[
                                        TextComponent(text='O3\n臭氧', weight='bold', size='lg', wrap=True, flex=1, gravity='center', color="#336699" if "臭氧" in arg['Pollutant'] else "#444444")
                                    ],
                                ),
                                BoxComponent(
                                    layout='vertical', flex=2,
                                    contents=[
                                        TextComponent(text='8小時\n移動平均', size='sm', wrap=True, flex=1, gravity='center', align="end"),
                                        TextComponent(text='小時濃度', size='sm', wrap=True, flex=1, gravity='center', align="end")
                                    ],
                                ),
                                BoxComponent(
                                    layout='vertical', flex=2,
                                    contents=[
                                        TextComponent(text=arg['O3_8hr'], weight='bold', size='xxl', wrap=True, flex=1, gravity='center', align="end"),
                                        TextComponent(text=arg['O3'], weight='bold', size='xxl', wrap=True, flex=1, gravity='center', align="end")
                                    ],
                                )
                            ],
                        ),
                        # PM2.5 細懸浮微粒
                        SeparatorComponent(margin='md'),
                        BoxComponent(
                            layout='horizontal',
                            margin='md',
                            contents=[
                                BoxComponent(
                                    layout='vertical', flex=3,
                                    contents=[
                                        TextComponent(text='PM2.5\n細懸浮微粒', weight='bold', size='lg', wrap=True, flex=1, gravity='center', color="#336699" if "臭氧" in arg['Pollutant'] else "#444444")
                                    ],
                                ),
                                BoxComponent(
                                    layout='vertical', flex=2,
                                    contents=[
                                        TextComponent(text='移動平均', size='sm', wrap=True, flex=1, gravity='center', align="end"),
                                        TextComponent(text='小時濃度', size='sm', wrap=True, flex=1, gravity='center', align="end")
                                    ],
                                ),
                                BoxComponent(
                                    layout='vertical', flex=2,
                                    contents=[
                                        TextComponent(text=arg['PM2.5_AVG'], weight='bold', size='xxl', wrap=True, flex=1, gravity='center', align="end"),
                                        TextComponent(text=arg['PM2.5'], weight='bold', size='xxl', wrap=True, flex=1, gravity='center', align="end")
                                    ],
                                )
                            ],
                        ),
                        # PM10 懸浮微粒
                        SeparatorComponent(margin='md'),
                        BoxComponent(
                            layout='horizontal',
                            margin='md',
                            contents=[
                                BoxComponent(
                                    layout='vertical', flex=3,
                                    contents=[
                                        TextComponent(text='PM10\n懸浮微粒', weight='bold', size='lg', wrap=True, flex=1, gravity='center', color="#336699" if "臭氧" in arg['Pollutant'] else"#444444")
                                    ],
                                ),
                                BoxComponent(
                                    layout='vertical', flex=2,
                                    contents=[
                                        TextComponent(text='移動平均', size='sm', wrap=True, flex=1, gravity='center', align="end"),
                                        TextComponent(text='小時濃度', size='sm', wrap=True, flex=1, gravity='center', align="end")
                                    ],
                                ),
                                BoxComponent(
                                    layout='vertical', flex=2,
                                    contents=[
                                        TextComponent(text=arg['PM10_AVG'], weight='bold', size='xxl', wrap=True, flex=1, gravity='center', align="end"),
                                        TextComponent(text=arg['PM10'], weight='bold', size='xxl', wrap=True, flex=1, gravity='center', align="end")
                                    ],
                                )
                            ],
                        ),
                        # CO 一氧化碳
                        SeparatorComponent(margin='md'),
                        BoxComponent(
                            layout='horizontal',
                            margin='md',
                            contents=[
                                BoxComponent(
                                    layout='vertical', flex=3,
                                    contents=[
                                        TextComponent(text='PM10\n懸浮微粒', weight='bold', size='lg', wrap=True, flex=1, gravity='center', color="#336699" if "臭氧" in arg['Pollutant'] else"#444444")
                                    ],
                                ),
                                BoxComponent(
                                    layout='vertical', flex=2,
                                    contents=[
                                        TextComponent(text='8小時\n移動平均', size='sm', wrap=True, flex=1, gravity='center', align="end"),
                                        TextComponent(text='小時濃度', size='sm', wrap=True, flex=1, gravity='center', align="end")
                                    ],
                                ),
                                BoxComponent(
                                    layout='vertical', flex=2,
                                    contents=[
                                        TextComponent(text=arg['CO_8hr'], weight='bold', size='xxl', wrap=True, flex=1, gravity='center', align="end"),
                                        TextComponent(text=arg['CO'], weight='bold', size='xxl', wrap=True, flex=1, gravity='center', align="end")
                                    ],
                                )
                            ],
                        ),
                        # SO2 二氧化硫
                        SeparatorComponent(margin='md'),
                        BoxComponent(
                            layout='horizontal',
                            margin='md',
                            contents=[
                                BoxComponent(
                                    layout='vertical', flex=3,
                                    contents=[
                                        TextComponent(text='SO2\n二氧化硫', weight='bold', size='lg', wrap=True, flex=1, gravity='center', color="#336699" if "臭氧" in arg['Pollutant'] else"#444444")
                                    ],
                                ),
                                BoxComponent(
                                    layout='vertical', flex=2,
                                    contents=[
                                        TextComponent(text='移動平均', size='sm', wrap=True, flex=1, gravity='center', align="end"),
                                        TextComponent(text='小時濃度', size='sm', wrap=True, flex=1, gravity='center', align="end")
                                    ],
                                ),
                                BoxComponent(
                                    layout='vertical', flex=2,
                                    contents=[
                                        TextComponent(text=arg['SO2_AVG'], weight='bold', size='xxl', wrap=True, flex=1, gravity='center', align="end"),
                                        TextComponent(text=arg['SO2'], weight='bold', size='xxl', wrap=True, flex=1, gravity='center', align="end")
                                    ],
                                )
                            ],
                        ),
                        # NO2 二氧化氮
                        SeparatorComponent(margin='md'),
                        BoxComponent(
                            layout='horizontal',
                            margin='md',
                            contents=[
                                BoxComponent(
                                    layout='vertical', flex=3,
                                    contents=[
                                        TextComponent(text='NO2\n二氧化氮', weight='bold', size='lg', wrap=True, flex=1, gravity='center', color="#336699" if "臭氧" in arg['Pollutant'] else"#444444")
                                    ],
                                ),
                                BoxComponent(
                                    layout='vertical', flex=2,
                                    contents=[
                                        TextComponent(text='小時濃度', size='sm', wrap=True, flex=1, gravity='center', align="end")
                                    ],
                                ),
                                BoxComponent(
                                    layout='vertical', flex=2,
                                    contents=[
                                        TextComponent(text=arg['NO2'], weight='bold', size='xxl', wrap=True, flex=1, gravity='center', align="end")
                                    ],
                                )
                            ],
                        )
                    ],
                ),
            )
