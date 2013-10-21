from .models import Game
from register.models import Player
from django.contrib.auth.models import User


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
        depth = 2






