from django.contrib.auth.models import User
from tastypie.resources import ModelResource,ALL, ALL_WITH_RELATIONS
from tastypie import fields

from game.models import Game
from register.models import Sport, Player

class SportResource(ModelResource):
    class Meta:
        queryset = Sport.objects.all()
        resource_name = 'sport'
        allowed_methods = ['get']
        include_resource_uri = False
        excludes = ['id']
        filtering = {
            'sport': ('exact')
        }

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['password', 'is_active', 'is_staff', 'is_superuser', 'id']
        allowed_methods = ['get']
        include_resource_uri = False
        allowed_methods = ['get']
        filtering = {
            'username': ALL,
            'email': ALL
        }

class PlayerResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user', full=True)
    sports = fields.ManyToManyField(SportResource, 'sports', full=True)
    class Meta:
        include_resource_uri = False
        queryset = Player.objects.all()
        resource_name = 'player'
        fields = ['sports', 'image_url', 'gender', 'user']
        allowed_methods = ['get']
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'gender' : ALL,
            'sports' : ALL_WITH_RELATIONS,
        }

class GameResource(ModelResource):
    sport = fields.ForeignKey(SportResource, 'sport', full=True)
    owner = fields.ForeignKey(UserResource, 'owner', full=True)
    players = fields.ManyToManyField(PlayerResource, 'players', full=True)
    class Meta:
        resource_name = 'game'
        queryset = Game.objects.all()
        include_resource_uri = False
        allowed_methods = ['get']
        filtering = {
            'game': ALL_WITH_RELATIONS,
            'owner': ALL_WITH_RELATIONS,
            'players' : ALL_WITH_RELATIONS,
            'sport' : ALL_WITH_RELATIONS,
        }
