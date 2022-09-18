from ast import Is, Raise
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

class ResolveAddressView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request, format=None):
    user_uid = str(request.data.get("user_uid"))
    #user_uid = "roM8dQofqKsyA2Y5wOf0hDJT66wRQhlQ"

    user = ANSUser.objects.get(user_uid = user_uid)
    print(user.blocked_enterprises.all(), request.user in user.blocked_enterprises.all())
    if request.user in user.blocked_enterprises.all():
      return Response({'message': "PermissionDenied: Not found in requested users' trusted enterprises."})

    if request.user in user.pending_enterprises.all():
      return Response({'message': "PendingRequest: User authentication for request is pending."})

    if request.user in user.trusted_enterprises.all():
      return Response({'address': user.address})
    else:
      device_token = "eznNW6guRRauQ9xSkU0Z5V:APA91bFKxiR8WW1oi-tIhxWixJpCl4c1jKNjgZBKjHOLc4-sT3_t1cQlPQ2NU2Accb1rlZJ98vAvszi3Tw-rl8SKGB8T-MbLLkCHXV6dzmpS3PpucmFRNfj-S-QmDeR1zU9XbI_xUpou"
      message = messaging.Message(
        data = {
          'company_email': request.user.email,
          'company_name': request.user.ansuser.enterprise_name,
        },
        token = device_token,
      )
      user.pending_enterprises.add(request.user)
      response = messaging.send(message)
      return Response({'message': "AuthRequest Sent: User authentication for request is pending."})

# class 

class EnterpriseTrustAuth(APIView):

  def post(self, request, format=None):
    data = request.data
    company_name, auth_user_uid, verdict = data['company_name'], data['auth_user_uid'], data['verdict']
    # print(company_name, auth_user_uid, verdict)
    auth_user = ANSUser.objects.get(user_uid = auth_user_uid)
    company_user = ANSUser.objects.get(enterprise_name = company_name)
    if verdict == "YES":
      assert(company_user not in auth_user.blocked_enterprises.all())
      if company_user.user in auth_user.pending_enterprises.all():
        auth_user.pending_enterprises.remove(company_user.user)

      if company_user.user in auth_user.trusted_enterprises.all():
        auth_user.trusted_enterprises.remove(company_user.user)
      
      auth_user.trusted_enterprises.add(company_user.user)
    elif verdict == "NO":
      if company_user.user in auth_user.pending_enterprises.all():
        auth_user.pending_enterprises.remove(company_user.user)
   
      if company_user.user in auth_user.trusted_enterprises.all():
        auth_user.trusted_enterprises.remove(company_user.user)

      if company_user.user not in auth_user.blocked_enterprises.all():
        auth_user.blocked_enterprises.add(company_user.user)

    return Response({})
