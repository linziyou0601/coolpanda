from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django import forms
from .models import PushMessages
from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from datetime import datetime
import psycopg2, pytz, json

line_bot_api = LineBotApi('HRWbC4w2S3J3JvFAQQkQnp4gxXVWtCwLWgrdanU72Y26+hwAoZvdiwhjyLPuIPdYLaqqy4ZDIC48EDGEo9FDp0VhS453OJfXEfFCwoFhZxhIFy6ESVLFr7fPuythQb4WA4gvEHkCjJ+yuMJDgzeR8gdB04t89/1O/w1cDnyilFU=')

class pushForm(forms.Form):  
    messageType = forms.ChoiceField()
    messageTitle = forms.CharField()
    messageContent = forms.CharField()

def getConnect():
    conn = psycopg2.connect(database="d6tkud0mtknjov", user="ifvbkjtshpsxqj", password="4972b22ed367ed7346b0107d3c3e97db14fac1dde628cd6d7f08cf502c927ee1", host="ec2-50-16-197-244.compute-1.amazonaws.com", port="5432")
    conn.autocommit = True
    return conn

def initalization():
    conn = getConnect()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS "pushMessages" (
            "id" SERIAL PRIMARY KEY,
            "message_type" TEXT NOT NULL,
            "message_title" TEXT NOT NULL,
            "message_content" TEXT NOT NULL,
            "create_at" TEXT NOT NULL
        )
    ''')
    conn.close()

def pushToLine(type, title, content):
    conn = getConnect()
    c = conn.cursor()
    c.execute('SELECT * FROM users Where allowpush=1')
    data = c.fetchall()
    conn.close()
    users = data[0] if len(data) else []
    message = []
    if type == 'text':
        message = TextSendMessage(text='【' + title + '】\n' + content)
    elif type == 'flex':
        try:
            obj = json.loads(content)
            message = FlexSendMessage(alt_text=title, contents=obj)
        except:
            return False
    else:
        if 'https://' in content and any(x in content for x in ['.jpg','.jpeg','.png']):
            message = ImageSendMessage(original_content_url=content, preview_image_url=content)
        else:
            return False
    line_bot_api.push_message(users, message)
    return True

# Create your views here.
@method_decorator(login_required, name='dispatch')
class pushView(TemplateView):
    template_name = 'pushMessage/pushMessage.html'

    def get(self, request):
        initalization() 
        form = pushForm()
        allPushes= PushMessages.objects.all()[:5]
        args = {'form': form, 'allPushes': allPushes, 'validStr': ""}
        return render( request, self.template_name, args)

    def post(self, request):    
        form = pushForm(request.POST)
        validStr = "" 
        if form.is_valid():
            messageType = form.cleaned_data['messageType']
            messageTitle = form.cleaned_data['messageTitle']
            messageContent = form.cleaned_data['messageContent']
            createAt = str(datetime.now(pytz.timezone("Asia/Taipei")))
            if pushToLine(messageType, messageTitle, messageContent):
                conn = getConnect()
                c = conn.cursor()
                c.execute('INSERT INTO "pushMessages" (message_type, message_title, message_content, create_at) VALUES(%s,%s,%s,%s)', 
                        [messageType, messageTitle, messageContent, createAt])
                conn.close()
            else:
                validStr = "訊息格式有誤。"
            form = pushForm()
        allPushes= PushMessages.objects.all()[:5]
        args = {'form': form, 'allPushes': allPushes, 'validStr': validStr}      
        return render(request, self.template_name, args)