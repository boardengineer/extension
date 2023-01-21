from django.db import models
from users.models import User

import datetime

# Create your models here.
class Player(models.Model):
    user = models.ForeignKey(User, related_name='sts_player', on_delete=models.CASCADE)
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

    boss_name = models.CharField(max_length=50, default="")

    relic_update_time = models.DateTimeField(default=datetime.datetime.now, blank=True)
    map_update_time = models.DateTimeField(default=datetime.datetime.now, blank=True)
    deck_update_time = models.DateTimeField(default=datetime.datetime.now, blank=True)


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


class MapNode(models.Model):
    owner = models.ForeignKey(Player, related_name="map_nodes", on_delete=models.CASCADE)

    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)

    offset_x = models.FloatField(default=0)
    offset_y = models.FloatField(default=0)

    symbol = models.CharField(max_length=5)


class MapEdge(models.Model):
    owner = models.ForeignKey(Player, related_name="map_edges", on_delete=models.CASCADE)

    source = models.IntegerField(default=0)
    destination = models.IntegerField(default=0)


class DecisionPrompt(models.Model):
    owner = models.ForeignKey(Player, related_name="decision_prompts", on_delete=models.CASCADE)


class DecisionOption(models.Model):
    prompt = models.ForeignKey(DecisionPrompt, related_name="options", on_delete=models.CASCADE)


class DecisionVote(models.Model):
    option = models.ForeignKey(DecisionOption, related_name="votes", on_delete=models.CASCADE)
