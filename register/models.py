from django.db import models
from django.contrib.auth.models import User


GENDER_CHOICES = (
        (u'Q', u'Undisclosed'),
        (u'M', u'Male'),
        (u'F', u'Female'),
    )


class Sport(models.Model):
    """ This will store the sport they are interested in playing in.

    """
    sport = models.CharField(max_length=30)

    def __unicode__(self):
        return "%s" % self.sport

    class Meta:
        verbose_name_plural = "Sports"


class Player(models.Model):
    """ This class will respresent all the information associated with player.

    Keyword arguments:

    """
    user = models.ForeignKey(User, blank=True, null=True)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, blank=True)
    sports = models.ManyToManyField('Sport')
    twitter_oauth_token = models.CharField(max_length=150, blank=True)
    twitter_oauth_secret = models.CharField(max_length=150, blank=True)
    facebook_oauth_token = models.CharField(max_length=150, blank=True)
    facebook_id = models.IntegerField(blank=True, null=True)
    image_url = models.CharField(max_length=150, blank=True)

    def __unicode__(self):
        return "%s player named %s" % (self.get_gender_display(), self.user.first_name)

    class Meta:
        verbose_name_plural = "Players"
