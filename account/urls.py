from django.urls import path

from account import views
from account.views import profile

urlpatterns = [
    path('profile', profile, name='profile'),
    path('login', views.Login.as_view(), name='login'),
]