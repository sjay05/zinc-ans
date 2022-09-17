from ast import Raise
from email import message
from urllib import request
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User, auth 
from django.http import JsonResponse
from django.contrib.auth import authenticate
from ans_site.models import *
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from firebase_admin import messaging

def generate_api_token(request):
  usrname = request.GET.get("usrname")
  user = User.objects.get(username = usrname)
  if Token.objects.filter(user = user).exists():
    Token.objects.filer(user = user).delete()
  
  token = Token.objects.create(user = user)
  data = {
    'token': token.key
  }
  print(data)
  return JsonResponse(data)

