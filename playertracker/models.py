from django.db import models

# Create your models here.
class Player(models.Model):
    twitch_username = models.CharField(max_length=50)
    player_current_hp = models.IntegerField()
    player_max_hp = models.IntegerField()
