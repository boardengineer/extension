from django.core.cache import cache
from django.db import transaction
from rest_framework import serializers
from playertracker.models import DecisionOption, DecisionPrompt, DecisionVote, Player, Relic, Card, MapNode, MapEdge

from datetime import datetime

class DecisionVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DecisionVote
        fields = ['option', 'twitch_user_id']

class DecisionOptionSerializer(serializers.ModelSerializer):
    prompt_id = serializers.IntegerField(required=False)

    class Meta:
        model = DecisionOption
        fields = ['id', 'x_pos', 'y_pos', 'height', 'width', 'value', 'prompt_id']


class DecisionPromptSerializer(serializers.ModelSerializer):
    options = DecisionOptionSerializer(many=True)
    user = serializers.IntegerField(required=False)

    class Meta:
        model = DecisionPrompt
        fields = ['options','user']


    def create(self, validated_data):
        obj = DecisionPrompt(owner_id=validated_data.get('user'))
        options = validated_data.get('options')
        
        with transaction.atomic():
            obj.save()
            if options is not None:
                for option in options:
                    option['prompt_id'] = obj.id
                    option_serializer = DecisionOptionSerializer(data=option)
                    if option_serializer.is_valid():
                        option_serializer.save()

        return obj


class CardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Card
        fields = ['name', 'description']


class MapNodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MapNode
        fields = ['x', 'y', 'offset_x', 'offset_y', 'symbol']


class MapEdgeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MapEdge
        fields = ['source', 'destination']


class RelicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Relic
        fields = ['name', 'description', 'x_pos', 'y_pos','height', 'width']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)

        instance.x_pos = validated_data.get('x_pos', instance.x_pos)
        instance.y_pos = validated_data.get('y_pos', instance.y_pos)

class MinPlayerSerializer(serializers.ModelSerializer):
    deck_update_time = serializers.SerializerMethodField()
    map_update_time = serializers.SerializerMethodField()
    relic_update_time = serializers.SerializerMethodField()
    decision_update_time = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ['user',
                'screen_height', 'screen_width',
                'map_button_x', 'map_button_y','map_button_height', 'map_button_width', 'boss_name',
                'deck_button_x', 'deck_button_y','deck_button_height', 'deck_button_width', 'deck_update_time',
                'map_update_time', 'relic_update_time', 'decision_update_time']

    def get_deck_update_time(self, instance):
        return int(datetime.timestamp(instance.deck_update_time)) + 1

    def get_map_update_time(self, instance):
        return int(datetime.timestamp(instance.map_update_time)) + 1

    def get_relic_update_time(self,instance):
        return int(datetime.timestamp(instance.relic_update_time)) + 1

    def get_decision_update_time(self,instance):
        return int(datetime.timestamp(instance.decision_update_time)) + 1


class NukingPlayerSerializer(serializers.ModelSerializer):
    relics = RelicSerializer(many=True, required=False)
    deck = CardSerializer(many=True, required=False)
    map_nodes = MapNodeSerializer(many=True, required=False)
    map_edges = MapEdgeSerializer(many=True, required=False)
    decision_prompts = DecisionPromptSerializer(many=True, required=False)
    deck_update_time = serializers.SerializerMethodField()
    map_update_time = serializers.SerializerMethodField()
    relic_update_time = serializers.SerializerMethodField()
    decision_update_time = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ['user',
                'player_current_hp', 'player_max_hp',
                'screen_height', 'screen_width',
                'map_button_x', 'map_button_y','map_button_height', 'map_button_width', 'boss_name',
                'deck_button_x', 'deck_button_y','deck_button_height', 'deck_button_width',
                'relic_update_time', 'map_update_time', 'deck_update_time', 'decision_update_time',
                'map_nodes', 'map_edges',
                'relics', 'deck', 'decision_prompts']
    

    def get_deck_update_time(self, instance):
        return int(datetime.timestamp(instance.deck_update_time)) + 1

    def get_map_update_time(self, instance):
        return int(datetime.timestamp(instance.map_update_time)) + 1

    def get_relic_update_time(self,instance):
        return int(datetime.timestamp(instance.relic_update_time)) + 1

    def get_decision_update_time(self,instance):
        return int(datetime.timestamp(instance.decision_update_time)) + 1

    def update(self, instance, validated_data):
        #instance.user = validated_data.get('twitch_username', instance.twitch_username)
        instance.player_current_hp = validated_data.get('player_current_hp', instance.player_current_hp)
        instance.player_max_hp = validated_data.get('player_max_hp', instance.player_max_hp)

        instance.screen_height = validated_data.get('screen_height', instance.screen_height)
        instance.screen_width = validated_data.get('screen_width', instance.screen_width)

        instance.map_button_x = validated_data.get('map_button_x', instance.map_button_x)
        instance.map_button_y = validated_data.get('map_button_y', instance.map_button_y)
        instance.map_button_height = validated_data.get('map_button_height', instance.map_button_height)
        instance.map_button_width = validated_data.get('map_button_width', instance.map_button_width)
        instance.boss_name = validated_data.get('boss_name', instance.boss_name)

        instance.deck_button_x = validated_data.get('deck_button_x', instance.deck_button_x)
        instance.deck_button_y = validated_data.get('deck_button_y', instance.deck_button_y)
        instance.deck_button_height = validated_data.get('deck_button_height', instance.deck_button_height)
        instance.deck_button_width = validated_data.get('deck_button_width', instance.deck_button_width)

        invalidate_relics = False
        invalidate_deck = False
        invalidate_nodes = False
        invalidate_edges = False
        invalidate_decision = False

        relics = validated_data.get('relics')
        if relics is not None:
            with transaction.atomic():
                instance.relic_update_time = datetime.now()
                Relic.objects.filter(owner=instance).delete()
                for relic in relics:
                    relic_serializer = RelicSerializer(data=relic)
                    if relic_serializer.is_valid():
                        relic_serializer.save(owner=instance)
                invalidate_relics = True
        

        deck = validated_data.get('deck')
        if deck is not None:
            with transaction.atomic():
                Card.objects.filter(owner=instance).delete()
                instance.deck_update_time = datetime.now()
                for card in deck:
                    saved_card = Card(owner=instance)

                    saved_card.name = card.get('name', saved_card.name)
                    saved_card.description = card.get('description', saved_card.description)

                    saved_card.save() 
                invalidate_deck = True

        map_nodes = validated_data.get('map_nodes')
        if map_nodes is not None:
            with transaction.atomic():
                instance.map_update_time = datetime.now()
                MapNode.objects.filter(owner=instance).delete()
                for map_node in map_nodes:
                    saved_node = MapNode(owner=instance)

                    saved_node.x = map_node.get('x', saved_node.x)
                    saved_node.y = map_node.get('y', saved_node.y)

                    saved_node.offset_x = map_node.get('offset_x', saved_node.offset_x)
                    saved_node.offset_y = map_node.get('offset_y', saved_node.offset_y)

                    saved_node.symbol = map_node.get('symbol', saved_node.symbol)

                    saved_node.save()
                invalidate_nodes = True


        map_edges = validated_data.get('map_edges')
        if map_edges is not None:
            with transaction.atomic():
                instance.map_update_time = datetime.now()
                MapEdge.objects.filter(owner=instance).delete()
                for map_edge in map_edges:
                    saved_edge = MapEdge(owner=instance)

                    saved_edge.source = map_edge.get('source', saved_edge.source)
                    saved_edge.destination = map_edge.get('destination', saved_edge.destination)
            
                    saved_edge.save()
                invalidate_edges = True

        decision_prompts = validated_data.get('decision_prompts')
        if decision_prompts is not None:
            with transaction.atomic():
                instance.decision_update_time = datetime.now()
                DecisionPrompt.objects.filter(owner=instance).delete()
                for prompt in decision_prompts:
                    prompt['user'] = instance.id
                    prompt_serializer = DecisionPromptSerializer(data=prompt)
                    if prompt_serializer.is_valid():
                        prompt_serializer.save()
                invalidate_decision = True
        
        instance.save()

        if invalidate_relics:
            result_relics = []
            for relic in relics:
                result_relics.append(dict(relic))
            relics_cache_key = str(instance.user.channel_id) + 'RELICS'
            cache.set(relics_cache_key, result_relics, 300)
 
        if invalidate_deck:
            result_deck = []
            for card in deck:
                result_deck.append(dict(card))
            deck_cache_key = str(instance.user.channel_id) + 'DECK'
            cache.set(deck_cache_key, result_deck, 300)

        if invalidate_nodes:
            result_nodes = []
            for node in map_nodes:
                result_nodes.append(dict(node))
            nodes_cache_key = str(instance.user.channel_id) + 'NODES'
            cache.set(nodes_cache_key, result_nodes, 300)

        if invalidate_edges:
            result_edges = []
            for edge in map_edges:
                result_edges.append(dict(edge))
            edges_cache_key = str(instance.user.channel_id) + 'EDGES'
            cache.set(edges_cache_key, result_edges, 300)

        if invalidate_decision:
            result_prompts = []
            for prompt in decision_prompts:
                result_prompt = dict(prompt)
                new_options = result_prompt['options']
                for option in new_options:
                    option['id'] = option['prompt_id']
                    option.pop('prompt_id', None)
                result_prompt['options'] = new_options
                
                result_prompts.append(result_prompt)
            decisions_cache_key = str(instance.user.channel_id) + 'DECISION'
            cache.set(decisions_cache_key, result_prompts, 300)

        return instance
