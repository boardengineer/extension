from django.db import models

# Create your models here.
class Player(models.Model):
    twitch_username = models.CharField(max_length=50)
    player_current_hp = models.IntegerField()
    player_max_hp = models.IntegerField()


class Relic(models.Model):
    owner = models.ForeignKey(Player, related_name='relics', on_delete=models.CASCADE)

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    x_pos = models.FloatField()
    y_pos = models.FloatField()
