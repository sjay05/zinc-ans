from django.urls import path, include
from ans_site.views.user import *
from ans_site.views.functions import *

urlpatterns = [
  path('', HomeView.as_view(), name="index"),
  path('login', LoginView.as_view(), name="login"),
  path('logout', LogoutView.as_view(), name="logout"),
  path('register', RegisterView.as_view(), name="register")
  
]