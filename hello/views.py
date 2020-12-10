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
    return HttpResponse('Webhook received', status=200)
