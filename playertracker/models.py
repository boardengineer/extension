from django.db import models

# Create your models here.
class Player(models.Model):
    twitch_username = models.CharField(max_length=50)
    player_current_hp = models.IntegerField(default=0)
    player_max_hp = models.IntegerField(default=0)

    # UI elements
    screen_height = models.FloatField(default=0)
    screen_width = models.FloatField(default=0)

    # Map button
    map_button_x = models.FloatField(default=0)
    map_button_y = models.FloatField(default=0)
    map_button_width = models.FloatField(default=0)
    map_button_height = models.FloatField(default=0)

    # Deck button
    deck_button_x = models.FloatField(default=0)
    deck_button_y = models.FloatField(default=0)
    deck_button_width = models.FloatField(default=0)
    deck_button_height = models.FloatField(default=0)


class Relic(models.Model):
    owner = models.ForeignKey(Player, related_name='relics', on_delete=models.CASCADE)

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    x_pos = models.FloatField(default=0)
    y_pos = models.FloatField(default=0)

    height = models.FloatField(default=0)
    width = models.FloatField(default=0)

class Card(models.Model):
    owner = models.ForeignKey(Player, related_name='deck', on_delete=models.CASCADE)

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
