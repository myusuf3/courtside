from django.core.management.base import BaseCommand
from game.models import Game


class Command(BaseCommand):
    """
    This is a management command that marks games as inactive
    after they have happened.
    """
    args = ''
    help = 'Cleans up finished game from the system'

    def handle(self, *args, **kwargs):
        games = Game.objects.filter(active=True).values('id')
        games = [game['id'] for game in games]
        print games
        CleanGamesTask().delay(games)
