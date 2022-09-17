from tkinter import W
from django.shortcuts import render, redirect
from django.views import View 
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate

class HomeView(View):
  context = {}
  template_name = "home_page.html"
  
  def get(self, request, *args, **kwargs):
    self.context['user'] = request.user
    self.template_name = "home_page.html"
    user = request.user
    
    return render(request, self.template_name, self.context)

class UpdateProfileView(View):
  template_name, context = "update_profile.html", {}

  def get(self, request, *args, **kwargs):
    self.context['user'] = request.user
    self.context['email'] = request.user.email
    self.context['address'] = request.user.ansuser.address
    self.context['enterprise_name'] = request.user.ansuser.enterprise_name

    return render(request, self.template_name, self.context)

  def post(self, request, *args, **kwargs):
    data, user = request.POST, request.user 
    if data.get("email") != "":
      user.email = data.get("email")
      user.save()
    
    if user.ansuser.is_home_owner and data.get("address") != "":
        user.ansuser.address = data.get("address")
        user.ansuser.save()
    
    if user.ansuser.is_enterprise and data.get("enterprise_name") != "":
      user.ansuser.enterprise_name = data.get("enterprise_name")
      user.ansuser.save()

    return redirect("update_profile")