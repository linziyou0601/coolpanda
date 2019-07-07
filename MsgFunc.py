from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton
)

def msgFunc(stri, arg=[]):
    if stri=="main":
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
                            TextComponent(text='牛批熊貓主選單', weight='bold', size='xl'),
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
                                                text='胡言亂語、抽籤、算數、查詢時間',
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
                                            ),
                                        ],
                                    ),
                                    TextComponent(text=arg[0], wrap=True, color='#aaaaaa', size='sm'),
                                    TextComponent(text=arg[1], wrap=True, color='#aaaaaa', size='sm')
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
                                    label='查看說話教學',
                                    text='如何學說話'
                                ),
                            ),
                            ButtonComponent(
                                style='link',
                                height='sm',
                                action=MessageAction(
                                    label='查看抽籤教學',
                                    text='抽籤教學'
                                ),
                            ),
                            ButtonComponent(
                                style='link',
                                height='sm',
                                action=MessageAction(
                                    label='目前時間',
                                    text='現在幾點'
                                ),
                            ),
                            ButtonComponent(
                                style='link',
                                height='sm',
                                action=MessageAction(
                                    label='今天日期',
                                    text='今天幾月幾號'
                                ),
                            ),
                            ButtonComponent(
                                style='link',
                                height='sm',
                                action=MessageAction(
                                    label='四則運算',
                                    text='98 * 87 + 6 + ( 4 ^ 2 ) '
                                ),
                            ),
                            SpacerComponent(size='sm')
                        ],
                        flex=0
                    ),
                )
    elif stri=="teach":
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
                                                text='其他聊天室新增的籤也會顯示！',
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
                                                text='點擊下方按鈕呈現各功能範例！',
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
                                    text='籤桶;籤桶名稱;甲子籤;乙丑籤;丙寅籤;丁卯籤;戊辰籤'
                                ),
                            ),
                            ButtonComponent(
                                style='link',
                                height='sm',
                                action=MessageAction(
                                    label='② 查看所有籤桶',
                                    text='所有籤桶'
                                ),
                            ),
                            ButtonComponent(
                                style='link',
                                height='sm',
                                action=MessageAction(
                                    label='③ 抽一支籤',
                                    text='抽籤;籤桶名稱'
                                ),
                            ),
                            ButtonComponent(
                                style='link',
                                height='sm',
                                action=MessageAction(
                                    label='④ 刪除籤',
                                    text='刪除;籤桶名稱;甲子籤;丁卯籤'
                                ),
                            ),
                            ButtonComponent(
                                style='link',
                                height='sm',
                                action=MessageAction(
                                    label='⑤ 刪除籤桶',
                                    text='刪除籤桶;籤桶名稱'
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
    elif stri=="howToTrain":
        return BubbleContainer(
                    direction='ltr',
                    body=BoxComponent(
                        layout='vertical',
                        contents=[
                            # title
                            TextComponent(text='教學', weight='bold', size='sm', color="#1DB446"),
                            TextComponent(text='如何教我說話', weight='bold', size='xxl', margin='md'),
                            TextComponent(text='本熊貓也會學習其他聊天室的語料！', wrap=True, color='#aaaaaa', size='sm'),
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
                                                text='單句對話',
                                                color='#aaaaaa',
                                                size='sm',
                                                flex=1
                                            ),
                                            TextComponent(
                                                text='學說話;內容;回答',
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
                                                text='連續對話',
                                                color='#aaaaaa',
                                                size='sm',
                                                flex=1
                                            ),
                                            TextComponent(
                                                text='學說話;對話1;對話2;對話N',
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
                                    label='查看範例',
                                    text='學說話;牛批牛批;本喵真牛批！'
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