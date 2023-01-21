from django.shortcuts import render
from django.core.cache import cache
from rest_framework import generics,status,viewsets
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from playertracker.models import Card,MapNode,MapEdge,Player,Relic
from playertracker.serializers import CardSerializer,MapEdgeSerializer,MapNodeSerializer,MinPlayerSerializer,NukingPlayerSerializer,RelicSerializer
from users.models import User

from datetime import datetime

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def readonly_player_list(request, channel_id):
    timestamp = int(request.query_params.get('timestamp',0))

    try:
        user = User.objects.get(channel_id=channel_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        player = Player.objects.get(user=user)
    except Player.DoesNotExist:
        return Response(status=stats.HTTP_404_NOT_FOUND)

    player_cache_key = channel_id + 'PLAYER'
    if cache.get(player_cache_key) is not None:
        result_data = cache.get(player_cache_key)
    else:
        print('fresh')
        serializer = MinPlayerSerializer(player, context={'request':request})
        cache.set(player_cache_key, serializer.data, 300)
        result_data = serializer.data

    if timestamp < datetime.timestamp(player.relic_update_time):
        relics_cache_key = channel_id + 'RELICS'

        if cache.get(relics_cache_key) is not None:
            result_data['relics'] = cache.get(relics_cache_key)
        else:
            relics = Relic.objects.filter(owner=player)
            relics_json = []
            for relic in relics:
                relic_serializer = RelicSerializer(relic)
                relics_json.append(relic_serializer.data)
            result_data['relics'] = relics_json
            cache.set(relics_cache_key, relics_json, 300)

    if timestamp < datetime.timestamp(player.map_update_time):
        nodes_cache_key = channel_id + 'NODES'
        if cache.get(nodes_cache_key) is not None:
            result_data['map_nodes'] = cache.get(nodes_cache_key)
        else:
            nodes = MapNode.objects.filter(owner=player)
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

    if timestamp < datetime.timestamp(player.deck_update_time):
        deck_cache_key = channel_id + 'DECK'
        if cache.get(deck_cache_key) is not None:
            result_data['deck'] = cache.get(deck_cache_key)
        else:
            cards = Card.objects.filter(owner=player)
            deck_json = []
            for card in cards:
                card_serializer = CardSerializer(card)
                deck_json.append(card_serializer.data)
            result_data['deck'] = deck_json
            cache.set(deck_cache_key, deck_json, 300)

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
        cache.delete(str(player.user.channel_id) + 'PLAYER')
        serializer = NukingPlayerSerializer(player, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        player.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def get_player(channel_id):
    return "hello"
