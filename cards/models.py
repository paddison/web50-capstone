from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class User(AbstractUser):
    pass

class Card(models.Model):
    english = models.CharField(max_length=45)
    character = models.CharField(max_length=45)
    pinyin = models.CharField(max_length=45)
    comment = models.CharField(max_length=255)
    created_on = models.DateField(auto_now_add=True)
    due = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user), related_name='cards')


