from rest_framework import serializers
from playertracker.models import Player, Relic

class RelicSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ModelField(model_field=Relic()._meta.get_field('id'))

    class Meta:
        model = Relic
        fields = ['id','name', 'description', 'x_pos', 'y_pos','height', 'width']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)

        instance.x_pos = validated_data.get('x_pos', instance.x_pos)
        instance.y_pos = validated_data.get('y_pos', instance.y_pos)


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    relics = RelicSerializer(many=True)

    class Meta:
        model = Player
        fields = ['twitch_username', 'player_current_hp', 'player_max_hp', 'screen_height', 'screen_width', 'relics']

    def update(self, instance, validated_data):
        instance.twitch_username = validated_data.get('twitch_username', instance.twitch_username)
        instance.player_current_hp = validated_data.get('player_current_hp', instance.player_current_hp)
        instance.player_max_hp = validated_data.get('player_max_hp', instance.player_max_hp)

        instance.screen_height = validated_data.get('screen_height', instance.screen_height)
        instance.screen_width = validated_data.get('screen_width', instance.screen_width)

        relics = validated_data.get('relics')

        for relic in relics:
            relic_id = relic.get('id', None)
            if relic_id:
                saved_relic = Relic.objects.get(id=relic_id, owner=instance)

                saved_relic.name = relic.get('name', saved_relic.name)
                saved_relic.description = relic.get('description', saved_relic.description)
                
                saved_relic.x_pos = relic.get('x_pos', saved_relic.x_pos)
                saved_relic.y_pos = relic.get('y_pos', saved_relic.y_pos)

                saved_relic.height = relic.get('height', saved_relic.height)
                saved_relic.width = relic.get('width', saved_relic.width)

                saved_relic.save()

        instance.save()

        return instance


class NukingPlayerSerializer(serializers.HyperlinkedModelSerializer):
    relics = RelicSerializer(many=True)

    class Meta:
        model = Player
        fields = ['twitch_username', 'player_current_hp', 'player_max_hp', 'screen_height', 'screen_width', 'relics']

    def update(self, instance, validated_data):
        instance.twitch_username = validated_data.get('twitch_username', instance.twitch_username)
        instance.player_current_hp = validated_data.get('player_current_hp', instance.player_current_hp)
        instance.player_max_hp = validated_data.get('player_max_hp', instance.player_max_hp)

        instance.screen_height = validated_data.get('screen_height', instance.screen_height)
        instance.screen_width = validated_data.get('screen_width', instance.screen_width)

        print('should have deleted children')
        Relic.objects.filter(owner=instance).delete()

        relics = validated_data.get('relics')

        for relic in relics:
          saved_relic = Relic(owner=instance)

          saved_relic.name = relic.get('name', saved_relic.name)
          saved_relic.description = relic.get('description', saved_relic.description)
                
          saved_relic.x_pos = relic.get('x_pos', saved_relic.x_pos)
          saved_relic.y_pos = relic.get('y_pos', saved_relic.y_pos)

          saved_relic.height = relic.get('height', saved_relic.height)
          saved_relic.width = relic.get('width', saved_relic.width)

          saved_relic.save()

        instance.save()

        return instance
