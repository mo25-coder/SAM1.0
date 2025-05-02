from django.db import models

# Create your models here.

class ChatMessage(models.Model):
    session_id = models.CharField(max_length=255)
    role = models.CharField(max_length=10)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
