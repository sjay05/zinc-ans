import json
from tkinter import W
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from ans_site.models import *
import requests
import json

class HomeView(View):
  context = {}
  template_name = "about.html"
  
  def get(self, request, *args, **kwargs):
    self.context['user'] = request.user
    user = request.user
    if user.is_superuser:
      return render(request, "home_page.html", self.context)

    if user.is_authenticated:
      self.template_name = "update_profile.html"
      return redirect('update_profile')
    
    return redirect('about')
#    return render(request, self.template_name, self.context)

class UpdateProfileView(View):
  template_name, context = "update_profile.html", {}

  def get(self, request, *args, **kwargs):
    self.context['user'] = request.user
    self.context['email'] = request.user.email
    self.context['address'] = request.user.ansuser.address
    self.context['enterprise_name'] = request.user.ansuser.enterprise_name
    # print(self.context['enterprise_name'])

    return render(request, self.template_name, self.context)

  def post(self, request, *args, **kwargs):
    data, user = request.POST, request.user 
    if data.get("email") != "":
      user.email = data.get("email")
      user.save()

    if user.ansuser.is_home_owner and data.get("address") != user.ansuser.address:
        user.ansuser.address = data.get("address")
        user.ansuser.save()
        call_back_url = "http://127.0.0.1:5000/ans_callback"
        json_str = '{' + f'"msg": "Address Change Alert", "{user.ansuser.user_uid}": "Rodgers", "address": "{user.ansuser.address}"' + '}'
        json_obj = json.loads(json_str)
        hook_send = requests.post(call_back_url, json = json_obj)
    
    # print(user.ansuser.enterprise_name)
    if user.ansuser.is_enterprise and data.get("enterprise_name") != user.ansuser.enterprise_name:
      user.ansuser.enterprise_name = data.get("enterprise_name")
      user.ansuser.save()

    # print(user.ansuser.enterprise_name)

    return redirect("update_profile")

class APIDocsView(View):
  template_name, context = "api_docs.html", {}

  def get(self, request, *args, **kwargs):
    docs = APIDocs.objects.all()[0]
    self.context['description'] = docs.content
    return render(request, self.template_name, self.context)

class AboutView(View):
  template_name, context = "about.html", {}

  def get(self, request, *args, **kwargs):
    docs = APIDocs.objects.all()[1]
    self.context['description'] = docs.content
    return render(request, self.template_name, self.context)

class LiveVerifView(View):
  template_name, context = "live_verif.html", {}

  def get(self, request, *args, **kwargs):
    user = request.user

    if user.ansuser.is_enterprise:
      return HttpResponse('Unauthorized', status=401)
#      return render(request,"blocked","Enterprises cannot view this page.")

    self.context['trusted_enterprises'] = []
    self.context['blocked_enterprises'] = []
    self.context['pending_enterprises'] = []

    for id in range(len(user.ansuser.trusted_enterprises.all())):
      self.context['trusted_enterprises'].append(user.ansuser.trusted_enterprises.all()[id])

    for id in range(len(user.ansuser.blocked_enterprises.all())):
      self.context['blocked_enterprises'].append(user.ansuser.blocked_enterprises.all()[id])

    for id in range(len(user.ansuser.pending_enterprises.all())):
      self.context['pending_enterprises'].append(user.ansuser.pending_enterprises.all()[id])

    return render(request, self.template_name, self.context)

  def post(self, request, *args, **kwargs):
    data, user = request.POST, request.user
    company_name = data.get("obj_id")
    print(company_name)
    a_user = ANSUser.objects.get(enterprise_name = company_name)
    company_user = a_user.user

    if data.get("push_type") == "pending-trust":
      user.ansuser.pending_enterprises.remove(company_user)
      user.ansuser.trusted_enterprises.add(company_user)     

    if data.get("push_type") == "pending-block":
      user.ansuser.pending_enterprises.remove(company_user)
      user.ansuser.blocked_enterprises.add(company_user)    

    if data.get("push_type") == "trusted-block":
      user.ansuser.trusted_enterprises.remove(company_user)
      user.ansuser.blocked_enterprises.add(company_user)

    if data.get("push_type") == "blocked-trust":
      user.ansuser.blocked_enterprises.remove(company_user)
      user.ansuser.trusted_enterprises.add(company_user)    

    ##print(data.get("obj_id"), data.get("push_type"))
    return redirect('live_verif')