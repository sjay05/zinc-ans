from django.urls import path, include
from ans_site.views.user import *
from ans_site.views.functions import *
from ans_site.views.api import *

urlpatterns = [
  path('', HomeView.as_view(), name="index"),
  path('login', LoginView.as_view(), name="login"),
  path('logout', LogoutView.as_view(), name="logout"),
  path('register', RegisterView.as_view(), name="register"),
  path('update_profile', UpdateProfileView.as_view(), name="update_profile"),

  path('generate_api_token', generate_api_token, name="gen_api_token"),
]