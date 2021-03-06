from django.shortcuts import render
from django.http import HttpResponse
from .models import Greeting

from google_trans_new import google_translator

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
    CHECK = "[To:5130876]Bot_Translate"
    CHECK2 ="[To:5130876]"
    CHECK3 = "##"

    payload = decode_payload(request)
    messageChat = payload["webhook_event"]["body"]
#     FormACI = payload["webhook_event"]["from_account_id"]
    print(messageChat)

    #systax

    if not CHECK3 in messageChat:
        return HttpResponse('Webhook received', status=200)
#     elif CHECK3 != messageChat[0]:
#         return HttpResponse('Webhook received', status=200)

#     FormACI = payload["webhook_event"]["from_account_id"]
#     messageChat = messageChat.replace(CHECK,"\n")
#     messageChat = messageChat.replace(CHECK2,"\n")
    messageChat = messageChat.replace(CHECK3,"\n")

    #account_id bot not translate
    accountId = payload["webhook_event"]["account_id"]
    # get message from room id
    roomId = payload["webhook_event"]["room_id"]

    if accountId == ACCOUNT_ID_BOT:
        return HttpResponse('Webhook received', status=200)


    #translate message
    translator = google_translator()

    lang = detect(messageChat)

    locale = "vi"

    if lang == "vi":
        locale = "ja"

    translated = translator.translate(messageChat, lang_src=lang, lang_tgt=locale)

    messageChat_re = "[To:" + format(accountId) + "]\n" + format(translated)

    #Send Data back to chatwork
#     client = ch.ChatworkClient('fd0602c43dd83cae39e7ebfb08d5793d')

    client = ch.ChatworkClient('6ea469a41f584dc23c13f0f79c23d643')
    res = client.get_messages(room_id=roomId, force=True)

    # post message to room 1234
    client.post_messages(room_id=roomId, message=messageChat_re)

    return HttpResponse('Webhook received', status=200)