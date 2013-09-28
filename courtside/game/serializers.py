from .models import Game

from rest_framework import serializers

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = (
            'id',
            'owner',
            'sport',
            'start_date_and_time',
            'active',
            'restrictions'
            )