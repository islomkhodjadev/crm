from django.db import models
from company.models import Company
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey



class Alert(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=50, unique=True)
    data = models.FileField()
    instructions = models.TextField()



class TelegramBotManager(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    token = models.CharField(max_length=200)
    data = models.FileField()
    instructions = models.TextField()



class CommunicationPortal(models.Model):
    
    class TypePortal(models.TextChoices):
        TELEGRAM_BOT = "BOT", "Telegram bot"
        CALLS = "CAL", "Phone call"
        SMS = "SMS", "sms messaging"
        
    
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=3, choices=TypePortal.choices, default=TypePortal.CALLS)
    phone_number = models.CharField(max_length=50, unique=True)
    
    data = models.FileField()
    instructions = models.TextField()



class Message(models.Model):
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='messages')
    
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=models.Q(app_label='services', model='alert') | 
                          models.Q(app_label='services', model='telegrambotmanager') | 
                          models.Q(app_label='services', model='communicationportal')
    )
    
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    
   
    # If you have a Customer or Agent model, you might want to link the message to them as well.
    sender = models.ForeignKey('agent.Agent', on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_messages')
    recipient = models.ForeignKey('customer.Customer', on_delete=models.SET_NULL, null=True, blank=True, related_name='received_messages')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    received_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)

