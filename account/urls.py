from django.urls import path
from account.views import profile

urlpatterns = [
    path('profile', profile, name='profile'),
]