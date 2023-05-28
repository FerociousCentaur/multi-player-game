import uuid

from django.db import models


# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    uid = models.CharField(max_length=20, default=str(uuid.uuid4())[:7], blank=False,unique=True)
    cards = models.TextField(null=True,blank=True)

class Game(models.Model):
    room_code = models.CharField(max_length=20, default=str(uuid.uuid4())[:7], blank=False,unique=True)
    game_creator = models.CharField(max_length=100)
    players = models.ManyToManyField(Profile)
    is_over = models.BooleanField(default=False)
    is_in_progress = models.BooleanField(default=False)

    game_score = models.TextField(null=True,blank=True)
    folded_cards = models.TextField(null=True,blank=True)
    unfolded_cards = models.TextField(null=True,blank=True)
