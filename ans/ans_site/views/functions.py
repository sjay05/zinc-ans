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

