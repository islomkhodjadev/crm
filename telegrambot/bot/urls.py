from django.urls import path
from .views import BotListCreate

urlpatterns = [
    path('bots/', BotListCreate.as_view(), name='bot-list-create'),
]
