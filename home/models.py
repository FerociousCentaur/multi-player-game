from django.db import models
import uuid
# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=100,blank=False,null=False)
    uid = models.CharField(max_length=20,default=uuid.uuid4,blank=False)

class Game(models.Model):
    room_code = models.CharField(max_length=100)
    game_creator = models.CharField(max_length=100)
    players = models.ManyToManyField(Profile)
    is_over = models.BooleanField(default=False)
    is_in_progress = models.BooleanField(default=False)