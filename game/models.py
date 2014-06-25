from django.contrib.auth.models import User
from django.db import models
from register.models import Player, Sport


class Game(models.Model):
    """ This class represents the Game model.
    """
    players = models.ManyToManyField(Player)
    owner = models.ForeignKey(User)
    sport = models.ForeignKey(Sport)
    start_date_and_time = models.DateTimeField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.CharField(max_length=50)
    minimum_players = models.IntegerField()
    restrictions = models.CharField(max_length=200, blank=True)
    active = models.NullBooleanField()

    def __unicode__(self):
        return "%s - %s at %s" % (self.sport.sport, self.start_date_and_time, self.address)

    class Meta:
        verbose_name_plural = "Games"

