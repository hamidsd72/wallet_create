from unicodedata import name
from django.urls import path
from .views import Home, SetWallet

app_name = 'wallet'

urlpatterns = [
    path('', Home, name='home'),
    path('setWallet/<slug:slug>', SetWallet, name='setWallet'),
]
