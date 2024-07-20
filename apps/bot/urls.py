from django.urls import path
from bot.views import webhook

app_name = 'bot'

urlpatterns = [
    path('webhook/', webhook, name='webhook'),
]
