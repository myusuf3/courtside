from .models import Game
from .serializers import GameSerializer

from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response

class GameList(APIView):

    def get(self, request, format=None):
        games = Game.objects.filter(active=True)
        serialized_games = GameSerializer(games, many=True)
        return Response(serialized_games.data)

class GameDetail(APIView):

    def get_object(self, pk):
        try:
            return Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            raise Http404


    def get(self, request, pk, format=None):
        game = self.get_object(pk)
        serialized_game = GameSerializer(game)
        return Response(serialized_game.data)
