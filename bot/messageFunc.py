from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

##主選單
def flexMainMenu(arg=[]):
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
                                            text='胡言亂語、抽籤、擲筊、查氣象、查時間',
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
                                label='我要擲筊',
                                text='擲筊'
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

##抽籤式回應教學
def flexTeachLottery(arg=[]):
    return BubbleContainer(
                direction='ltr',
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        # title
                        TextComponent(text='教學', weight='bold', size='sm', color="#1DB446"),
                        TextComponent(text='抽籤式回覆', weight='bold', size='xxl', margin='md'),
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
                                            text='「牛批貓+關鍵字」或「抽籤+關鍵字」將會從「關鍵字」對應的所有詞條中，隨機抽出一個回答。',
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
                                label='範例步驟①',
                                text='學說話;抽神籤;甲子籤;乙丑籤;丙寅籤;丁卯籤;戊辰籤'
                            ),
                        ),
                        ButtonComponent(
                            style='link',
                            height='sm',
                            action=MessageAction(
                                label='範例步驟②',
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
def flexTeachChat(arg=[]):
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

##查氣象教學
def flexTeachCWB(arg=[]):
    return BubbleContainer(
                direction='ltr',
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        # title
                        TextComponent(text='教學', weight='bold', size='sm', color="#1DB446"),
                        TextComponent(text='查氣象', weight='bold', size='xxl', margin='md'),
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
                                            text='空氣品質',
                                            color='#aaaaaa',
                                            size='sm',
                                            flex=3
                                        ),
                                        TextComponent(
                                            text='「測站名+空氣/空汙/空氣品質/PM2.5」',
                                            wrap=True,
                                            color='#666666',
                                            size='sm',
                                            flex=6
                                        )
                                    ],
                                ),
                                BoxComponent(
                                    layout='baseline',
                                    spacing='sm',
                                    contents=[
                                        TextComponent(
                                            text='目前天氣',
                                            color='#aaaaaa',
                                            size='sm',
                                            flex=3
                                        ),
                                        TextComponent(
                                            text='「測站名+天氣/會下雨嗎」',
                                            wrap=True,
                                            color='#666666',
                                            size='sm',
                                            flex=6
                                        )
                                    ],
                                ),
                                BoxComponent(
                                    layout='baseline',
                                    spacing='sm',
                                    contents=[
                                        TextComponent(
                                            text='一週天氣',
                                            color='#aaaaaa',
                                            size='sm',
                                            flex=3
                                        ),
                                        TextComponent(
                                            text='「縣市名+一週天氣/明天天氣/明天會下雨嗎」',
                                            wrap=True,
                                            color='#666666',
                                            size='sm',
                                            flex=6
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
                                label='查目前天氣範例',
                                text='斗六天氣'
                            ),
                        ),
                        ButtonComponent(
                            style='link',
                            height='sm',
                            action=MessageAction(
                                label='查一週天氣範例',
                                text='斗六一週天氣'
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
def flexTeaching(arg=[]):
    return CarouselContainer(
        contents=[
            flexTeachChat(),
            flexTeachLottery(),
            flexTeachCWB()
        ]
    )

##狀態選單
def flexStatusMenu(arg=[]):
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
def flexWhatCanSay(arg=[]):
    #整理資料格式
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
    #建立容器
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
def flexAQI(arg={}):
    #整理資料格式
    arg['SiteName'] = arg['SiteName'][arg['SiteName'].index('(')+1:arg['SiteName'].index(')')] if '(' in arg['SiteName'] else arg['SiteName']
    arg['AQI'] = '-1' if arg['AQI']=='' else arg['AQI']
    for x in ['SO2', 'SO2_AVG', 'CO', 'CO_8hr', 'O3', 'O3_8hr', 'PM10', 'PM10_AVG', 'PM2.5', 'PM2.5_AVG', 'NO2']:
        arg[x] = 'NA' if arg[x]=='' else arg[x]
    AQIList = [[-1,"#888888"], [0,"#339933"], [51,"#EECC33"], [101,"#EE9933"], [151,"#DD3333"], [201,"#996699"], [301,"#990066"]]
    AQIcolor = list(filter(lambda x: int(arg['AQI'])>=x[0], AQIList))[::-1][0][1]
    #建立容器
    return BubbleContainer(
                direction='ltr',
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        # title
                        TextComponent(text=arg['Status'], weight='bold', size='sm', color=AQIcolor),
                        BoxComponent(
                            layout='horizontal',
                            margin='md',
                            contents=[
                                BoxComponent(
                                    layout='vertical', flex=5,
                                    contents=[
                                        TextComponent(text=arg['SiteName'], weight='bold', size='xxl'),
                                        TextComponent(text=arg['County'], weight='bold', size='lg', color="#333399")
                                    ],
                                ),
                                BoxComponent(
                                    layout='vertical', flex=3,
                                    contents=[
                                        TextComponent(text='AQI', size='lg', color=AQIcolor, align="end"),
                                        TextComponent(text=arg['AQI'] if arg['AQI']!='-1' else 'NA', weight='bold', size='4xl', color=AQIcolor, align="end")
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
                                        TextComponent(text='PM2.5\n細懸浮微粒', weight='bold', size='lg', wrap=True, flex=1, gravity='center', color="#336699" if "細懸浮微粒" in arg['Pollutant'] else "#444444")
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
                                        TextComponent(text='PM10\n懸浮微粒', weight='bold', size='lg', wrap=True, flex=1, gravity='center', color="#336699" if "懸浮微粒" in arg['Pollutant'].replace("細懸浮微粒","") else"#444444")
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
                                        TextComponent(text='PM10\n懸浮微粒', weight='bold', size='lg', wrap=True, flex=1, gravity='center', color="#336699" if "一氧化碳" in arg['Pollutant'] else"#444444")
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
                                        TextComponent(text='SO2\n二氧化硫', weight='bold', size='lg', wrap=True, flex=1, gravity='center', color="#336699" if "二氧化硫" in arg['Pollutant'] else"#444444")
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
                                        TextComponent(text='NO2\n二氧化氮', weight='bold', size='lg', wrap=True, flex=1, gravity='center', color="#336699" if "二氧化氮" in arg['Pollutant'] else"#444444")
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
                        ),
                        # 時間
                        SeparatorComponent(margin='md'),
                        BoxComponent(
                            layout='vertical',
                            margin='xs',
                            contents=[
                                TextComponent(
                                    text='截至'+arg['timeStr'],
                                    color='#aaaaaa',
                                    size='xs',
                                    align='end'
                                )
                            ],
                        )
                    ],
                ),
            )

##目前天氣
def flexWeather(arg={}):
    #整理資料格式
    arg['Temp'] = str(round(float(arg['Temp'])*10+0.5)/10) if arg['Temp']!='-99' else 'N/A'
    arg['Humd'] = str(round(float(arg['Humd'])*1000+0.5)/10) if arg['Humd']!='-99' else 'N/A'
    arg['24R'] = str(round(float(arg['24R'])*10+0.5)/10) if arg['24R']!='-99' else 'N/A'
    #建立容器
    return BubbleContainer(
                direction='ltr',
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        #溫度
                        TextComponent(
                            text=arg['Temp']+'°',
                            size='5xl',
                            align="center",
                            color="#990066"
                        ),
                        #天氣狀況描述
                        TextComponent(
                            text=arg['Wx'],
                            weight='bold',
                            size='lg',
                            align="center",
                            color="#990066"
                        ),
                        #目前天氣
                        BoxComponent(
                            layout='horizontal',
                            margin='xxl',
                            contents=[
                                #地區
                                BoxComponent(
                                    layout='vertical',
                                    flex=5,
                                    contents=[
                                        TextComponent(text=arg['locationName'], weight='bold', size='xxl', wrap=True),
                                        TextComponent(text=arg['City']+' '+arg['Town'], weight='bold', size='sm', color='#0D8186')
                                    ],
                                ),
                                #降雨率
                                BoxComponent(
                                    layout='vertical',
                                    flex=4,
                                    contents=[
                                        BoxComponent(
                                            layout='baseline',
                                            contents=[
                                                TextComponent(text='降雨率', weight='bold', size='sm', flex=2),
                                                TextComponent(text=arg['PoP6h']+'%', weight='bold', size='xl', color='#0D8186', flex=3)
                                            ],
                                        ),
                                        ##新API開放後才能顯示
                                        BoxComponent(
                                            layout='vertical',
                                            backgroundColor='#9FD8E3',
                                            height='10px',
                                            contents=[
                                                BoxComponent(
                                                    layout='vertical',
                                                    backgroundColor='#0D8186',
                                                    height='10px',
                                                    width=arg['PoP6h']+'%',
                                                    contents=[FillerComponent()],
                                                )
                                            ],
                                        )
                                    ],
                                )
                            ],
                        ),
                        SeparatorComponent(margin='md'),
                        #濕度、雨量
                        BoxComponent(
                            layout='horizontal',
                            margin='md',
                            contents=[
                                BoxComponent(
                                    layout='vertical',
                                    flex=5,
                                    contents=[
                                        TextComponent(text='濕度', size='sm', align='center'),
                                        TextComponent(text=arg['Humd']+'%', weight='bold', size='lg', align='center', color='#990066')
                                    ],
                                ),
                                SeparatorComponent(margin='md'),
                                BoxComponent(
                                    layout='vertical',
                                    flex=5,
                                    contents=[
                                        TextComponent(text='日積雨量', size='sm', align='center'),
                                        TextComponent(text=arg['24R']+' mm', weight='bold', size='lg', align='center', color='#990066')
                                    ],
                                )
                            ],
                        ),
                        SeparatorComponent(margin='md'),
                        #時間
                        BoxComponent(
                            layout='vertical',
                            margin='md',
                            contents=[
                                TextComponent(text='截至'+arg['TimeString'], size='sm', align='end', color='#AAAAAA')
                            ],
                        )
                    ],
                ),
            )

##未來天氣
def flexWeather72HR(arg):
    #整理資料格式
    WeatherList=[]
    for x in arg:
        WeatherList.append(BubbleContainer(
            direction='ltr',
            size='micro',
            body=BoxComponent(
                layout='vertical',
                contents=[
                    #Title
                    BoxComponent(
                        layout='horizontal',
                        contents=[
                            TextComponent(text=x['locationName'], size='sm', align='center', flex=4, color='#0D8186'),
                            TextComponent(text=x['startTime'][8:14]+'時', size='xs', align='center', flex=5, color='#1DB446')
                        ],
                    ),
                    #天氣內容
                    TextComponent(text=x['Temp']+'°', size='3xl', align='center', color='#990066'),
                    TextComponent(text=x['Wx'], size='sm', weight='bold', align='center', color='#990066'),
                    SeparatorComponent(margin='md'),
                    BoxComponent(
                        layout='horizontal',
                        margin='md',
                        contents=[
                            BoxComponent(
                                layout='vertical',
                                flex=5,
                                contents=[
                                    TextComponent(text='降雨率', size='xs', align='center', color='#666666'),
                                    TextComponent(text=x['PoP6h']+'%', weight='bold', size='md', align='center', color='#0D8186')
                                ],
                            ),
                            SeparatorComponent(margin='md'),
                            BoxComponent(
                                layout='vertical',
                                flex=5,
                                contents=[
                                    TextComponent(text='舒適度', size='xs', align='center', color='#666666'),
                                    TextComponent(text=x['CI'], weight='bold', size='md', align='center', color='#0D8186')
                                ],
                            )
                        ],
                    ),
                    SeparatorComponent(margin='md')
                ],
            ),
        ))
    
    #建立容器
    return CarouselContainer(contents = WeatherList)

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
                "action": {
                "type": "message",
                "label": "再擲一次",
                "text": "擲筊"
                },
                "style": "link",
                "color": "#ffffff"
            }
            ],
            "backgroundColor": "#c4241b"
        }
    }

