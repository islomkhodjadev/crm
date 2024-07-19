from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Bot
from .serializers import BotSerializer

class BotListCreate(generics.ListCreateAPIView):
    queryset = Bot.objects.all()
    serializer_class = BotSerializer
