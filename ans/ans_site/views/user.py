from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User, auth 
from django.contrib import messages
from django.contrib.auth import authenticate
from django.utils.crypto import get_random_string
from ans_site.models import *

class LoginView(View):
  template_name, context = "login.html", {}

  def get(self, request, *args, **kwargs):
    return render(request, self.template_name, self.context)
    
  def post(self, request, *args, **kwargs):
    data = request.POST
    username, pwd = data.get("username"), data.get("password")
    user = authenticate(username = username, password = pwd)

    if user is not None:
      auth.login(request, user)
      return redirect('/')
    else:
      messages.info(request, "Invalid Credentials")
      return redirect('login')

class RegisterView(View):
  template_name, context = "register.html", {}

  def get(self, request, *args, **kwargs):
    return render(request, self.template_name, self.context)

  def post(self, request, *args, **kwargs):
    data = request.POST
    username = data.get("username")
    email = data.get("email")
    pwd, pwd_check = data.get("password1"), data.get("password2")
    account_type = data.get("account_type")

    if pwd.__eq__(pwd_check):
      if User.objects.filter(username=username).exists():
        messages.info(request, "Username Taken")
        return redirect('register')
      else:
        user = User.objects.create_user(username = username, password = pwd)
        user.save()
        alphanumeric_id = get_random_string(length=32)
        while ANSUser.objects.filter(user_uid = alphanumeric_id).exists():
          alphanumeric_id = get_random_string(length=32)
        ANSUser.objects.create(user = user, is_enterprise = (account_type == "enterprise"), 
            is_home_owner = (account_type == "home_owner"), user_uid = alphanumeric_id)

        return redirect('login')
    else:
      messages.info(request, "Password doesn't match")
      return redirect('register')

class LogoutView(View):
  def get(self, request, *args, **kwargs):
    auth.logout(request)
    return redirect('/')