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
                                            flex=2
                                        ),
                                        TextComponent(
                                            text='壞壞',
                                            wrap=True,
                                            color='#825d5c',
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

##教學選單
def teaching(arg=[]):
    return CarouselContainer(
        contents=[
            teachChat(),
            teachLottery(),
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
            resList=[]
            for s in v:
                resList.append(TextComponent(text=s, color='#111111', size='sm', align='end', wrap=True))
            keywordObj.append(
                BoxComponent(
                    layout='horizontal', margin='md',
                    contents=[
                        TextComponent(text=k, color='#555555', size='sm', wrap=True, flex=1),
                        BoxComponent(
                            layout='vertical',
                            contents=resList,
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
                        # info
                        BoxComponent(
                            layout='horizontal',
                            margin='md',
                            contents=[
                                TextComponent(
                                    text='關鍵字數量',
                                    color='#555555',
                                    size='sm',
                                ),
                                TextComponent(
                                    text=arg[2],
                                    color='#111111',
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
                                    color='#555555',
                                    size='sm',
                                ),
                                TextComponent(
                                    text=arg[3],
                                    color='#111111',
                                    size='sm',
                                    align='end'
                                )
                            ],
                        ),
                        SeparatorComponent(margin='md'),
                        BoxComponent(
                            layout='vertical',
                            margin='md',
                            spacing='sm',
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