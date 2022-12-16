from rest_framework import serializers
from playertracker.models import Player

class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Player
        fields = ['twitch_username', 'player_current_hp', 'player_max_hp']

    def update(self, instance, validated_data):

        instance.twitch_username = validated_data.get('twitch_username', instance.twitch_username)
        instance.player_current_hp = validated_data.get('player_current_hp', instance.player_current_hp)
        instance.player_max_hp = validated_data.get('player_max_hp', instance.player_max_hp)

        instance.save()

        return instance
