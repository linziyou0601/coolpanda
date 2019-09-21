from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django import forms
from .models import PushMessages
from datetime import datetime
import psycopg2, pytz, json

class pushForm(forms.Form):  
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

# Create your views here.
@method_decorator(login_required, name='dispatch')
class pushView(TemplateView):
    template_name = 'pushMessage/pushMessage.html'

    def get(self, request):
        initalization() 
        form = pushForm()
        allPushes= PushMessages.objects.all()[:5]
        args = {'form': form, 'allPushes':allPushes}    
        return render( request, self.template_name, args)

    def post(self, request):    
        form = pushForm(request.POST)  
        if form.is_valid():
            messageType = 'text'
            messageTitle = form.cleaned_data['messageTitle']
            messageContent = form.cleaned_data['messageContent']
            createAt = str(datetime.now(pytz.timezone("Asia/Taipei")))
            conn = getConnect()
            c = conn.cursor()
            c.execute('INSERT INTO pushMessages(message_type, message_title, message_content, create_at) VALUES(%s,%s,%s,%s)', 
                      [messageType, messageTitle, messageContent, createAt])
            conn.close()
            form = pushForm()
        allPushes= PushMessages.objects.all()[:5]
        args = {'form': form, 'allPushes':allPushes}      
        return render(request, self.template_name, args)