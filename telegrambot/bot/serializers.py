from rest_framework import serializers
from .models import Bot

class BotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ['id', 'token', 'instructions', "api"]