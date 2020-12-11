from django.shortcuts import render
from django.http import HttpResponse
from .models import Greeting

from googletrans import Translator

from django.views.decorators.csrf import csrf_exempt
from langdetect import detect
import json
import pychatwork as ch
import re

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    payload = str(request.body, encoding='utf-8')
    return render(request, "index.html")
def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
# Create your views here.
def decode_payload(request):
    payload = str(request.body, encoding='utf-8')
    return json.loads(payload)

@csrf_exempt
def chatwork_webhook(request):

    ACCOUNT_ID_BOT = 5130876
    CHECK = "#"

    payload = decode_payload(request)
    messageChat = payload["webhook_event"]["body"]

    #systax translate
    if not CHECK in messageChat:
        return HttpResponse('Webhook received', status=200)
    elif CHECK != messageChat[0]:
        return HttpResponse('Webhook received', status=200)
    messageChat = messageChat.replace(CHECK,"")


    #account_id bot not translate
    accountId = payload["webhook_event"]["account_id"]
    if accountId == ACCOUNT_ID_BOT:
        return HttpResponse('Webhook received', status=200)


    #translate message
    #translator = Translator()

    #lang = detect(messageChat)

    #locale = "vi"
    #if lang == "vi":
    #    locale = "ja"

    #translated = translator.translate(messageChat, src=lang, dest=locale).text

    translator = Translator()
    t = translator.translate(messageChat, src='vi', dest='ja')



    #Send Data back to chatwork
    client = ch.ChatworkClient('fd0602c43dd83cae39e7ebfb08d5793d')

    # get message from room 1234
    res = client.get_messages(room_id='197925987', force=True)

    # post message to room 1234
    client.post_messages(room_id='197925987', message=t)


    return HttpResponse('Webhook received', status=200)
