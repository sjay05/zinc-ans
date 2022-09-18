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
  path('api_docs', APIDocsView.as_view(), name="api_docs"),
  path('live_verif', LiveVerifView.as_view(), name="live_verif"),
  path('about', AboutView.as_view(), name="about"),

  path('generate_api_token', generate_api_token, name="gen_api_token"),
  path('apiv1/resolve', ResolveAddressView.as_view(), name="resolve_address"),
  # path('apiv1/resolve/<str:user_uid>', ResolveAddressView.as_view(), name="resolve_address"),
  path('apiv1/trust_enterprise/', EnterpriseTrustAuth.as_view(), name="trust_enterprise"),
]

#   path('about', AboutView.as_view(), name="about"),