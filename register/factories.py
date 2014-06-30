import factory
import datetime

from game import models

from register.models import Player, Sport
from django.contrib.auth.models import User

class SportFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Sport

    sport = factory.Iterator(['soccer', 'basketball', 'volleyball', 'hockey', 'baseball'], cycle=False)


class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = User

    username = factory.Sequence(lambda n: 'username{0}'.format(n))
    first_name = factory.Sequence(lambda n: 'Mahdi{0}'.format(n))
    last_name = factory.Sequence(lambda n: 'Yusuf{0}'.format(n))
    email = factory.Sequence(lambda n: 'mahdi{0}@gmail.com'.format(n))


class PlayerFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Player

    user = factory.SubFactory(UserFactory)

    @factory.sequence
    def gender(n):
        if n % 2 == 0:
            return 'F'
        else:
            return 'M'

    @factory.post_generation
    def sports(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for sport in extracted:
                self.sports.add(sport)


class GameFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Game
    FACTORY_HIDDEN_ARGS = ('now',)

    now = factory.LazyAttribute(lambda o: datetime.datetime.utcnow())
    start_date_and_time = factory.LazyAttribute(lambda o: o.now + datetime.timedelta(days=4))
    latitude = factory.Sequence(lambda n: '45.{0}'.format(n))
    longitude = factory.Sequence(lambda n: '75.{0}'.format(n))
    minimum_players = 3


    @factory.sequence
    def active(n):
        return True

    @factory.post_generation
    def players(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for player in extracted:
                self.players.add(player)
