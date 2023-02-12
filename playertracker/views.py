import json

from django.shortcuts import render
from django.core.cache import cache
from django.http import QueryDict
from rest_framework import generics,status,viewsets
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from playertracker.models import Card, DecisionOption, DecisionPrompt, DecisionVote, MapNode,MapEdge,Player,Relic
from playertracker.serializers import CardSerializer, DecisionOptionSerializer, DecisionPromptSerializer, DecisionVoteSerializer, MapEdgeSerializer,MapNodeSerializer,MinPlayerSerializer,NukingPlayerSerializer,RelicSerializer
from users.models import User

from datetime import datetime


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def decision_query(request, prompt_id):
    cache_key = prompt_id + "DECISION_QUERY"
    if cache.get(cache_key) is not None:
        votes_json = cache.get(cache_key)
    else:
        options = DecisionOption.objects.filter(prompt=prompt_id)
        votes_json = []
        for option in options:
            votes = DecisionVote.objects.filter(option=option)
            for vote in votes:
                vote_serializer = DecisionVoteSerializer(vote)
                votes_json.append(vote_serializer.data)
        cache.set(cache_key, votes_json, 300)
    return Response(votes_json)


@api_view(['PUT'])
@authentication_classes([])
@permission_classes([])
def vote_view(request):
    params = json.loads(request.body)
    option = DecisionOption.objects.get(pk=params['option'])
    user_id = params['userId']
    DecisionVote.objects.filter(twitch_user_id=user_id).delete()

    vote = DecisionVote(option=option)
    vote.twitch_user_id = user_id
    vote.save()

    prompt_id = vote.option.prompt.id
    cache_key = str(prompt_id) + "DECISION_QUERY"
    cache.delete(cache_key)

    return Response('')

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def readonly_player_list(request, channel_id):
    timestamp = int(request.query_params.get('timestamp',0))
    player = None

    player_cache_key = channel_id + 'PLAYER'
    if cache.get(player_cache_key) is not None:
        result_data = cache.get(player_cache_key)
    else:
        print('FRESH PLAYER FETCH')
        try:
            user = User.objects.get(channel_id=channel_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if player is None:
            try:
                player = Player.objects.get(user=user)
            except Player.DoesNotExist:
                return Response(status=stats.HTTP_404_NOT_FOUND)

        serializer = MinPlayerSerializer(player, context={'request':request})
        cache_data = serializer.data
        cache_data['player'] = player.id
        cache.set(player_cache_key, cache_data, 300)
        result_data = cache_data

    if timestamp < result_data['relic_update_time']:
        relics_cache_key = channel_id + 'RELICS'

        if cache.get(relics_cache_key) is not None:
            result_data['relics'] = cache.get(relics_cache_key)
        else:
            relics = Relic.objects.filter(owner_id=result_data['player'])
            relics_json = []
            for relic in relics:
                relic_serializer = RelicSerializer(relic)
                relics_json.append(relic_serializer.data)
            result_data['relics'] = relics_json
            cache.set(relics_cache_key + " 2", relics_json, 300)

    if timestamp < result_data['map_update_time']:
        nodes_cache_key = channel_id + 'NODES'
        if cache.get(nodes_cache_key) is not None:
            result_data['map_nodes'] = cache.get(nodes_cache_key)
        else:
            nodes = MapNode.objects.filter(owner_id=result_data['player'])
            nodes_json = []
            for node in nodes:
                node_serializer = MapNodeSerializer(node)
                nodes_json.append(node_serializer.data)
            result_data['map_nodes'] = nodes_json
            cache.set(nodes_cache_key, nodes_json, 300)

        edges_cache_key = channel_id + 'EDGES'
        if cache.get(edges_cache_key) is not None:
            result_data['map_edges'] = cache.get(edges_cache_key)
        else:
            edges = MapEdge.objects.filter(owner=player)
            edges_json = []
            for edge in edges:
                edge_serializer = MapEdgeSerializer(edge)
                edges_json.append(edge_serializer.data)
            result_data['map_edges'] = edges_json
            cache.set(edges_cache_key, edges_json, 300)

    if timestamp < result_data['deck_update_time']:
        deck_cache_key = channel_id + 'DECK'
        if cache.get(deck_cache_key) is not None:
            result_data['deck'] = cache.get(deck_cache_key)
        else:
            cards = Card.objects.filter(owner_id=result_data['player'])
            deck_json = []
            for card in cards:
                card_serializer = CardSerializer(card)
                deck_json.append(card_serializer.data)
            result_data['deck'] = deck_json
            cache.set(deck_cache_key, deck_json, 300)

    if timestamp < result_data['decision_update_time']:
        decision_cache_key = channel_id + "DECISION"
        if cache.get(decision_cache_key) is not None:
            result_data['decision_prompts'] = cache.get(decision_cache_key)
        else:
            prompts = DecisionPrompt.objects.filter(owner_id=result_data['player'])
            prompts_json = []
            for prompt in prompts:
                prompt_serializer = DecisionPromptSerializer(prompt)
                prompts_json.append(prompt_serializer.data)
            result_data['decision_prompts'] = prompts_json
            cache.set(decision_cache_key, prompts_json, 300)

    return Response(result_data)


@api_view(['GET','PUT','DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_player_view(request):
    try:
        player = Player.objects.get(user=request.user)
    except Player.DoesNotExist:
        return Response(status=statusl.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PlayerSerializer(player)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = NukingPlayerSerializer(player, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete(str(player.user.channel_id) + 'PLAYER')
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        player.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

