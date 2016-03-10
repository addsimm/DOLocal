from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

import random

from mezzanine.core.models import TimeStamped

# Create your models here.

def pick_game_number():
    game_number = random.randrange(1, 75, 1)
    return game_number


class JoingoCard(TimeStamped, models.Model):
    class Meta:
        verbose_name = 'Joingo Card'
        verbose_name_plural = 'Joingo Cards'

    card_serial = models.PositiveIntegerField()
    entries = ArrayField(models.IntegerField(), default=None, size=25, null=True)
    tags = ArrayField(models.CharField(max_length=200))

    # card_owner_team = models.ForeignKey(JoingoTeam)



class JoingoTeam():
    team_name = models.CharField(max_length=30)
    # team_players


class JoingoGame():
    pass


class JoingoPlayer():
    player_user = models.OneToOneField(User, on_delete=models.CASCADE)
    # player_teams = models.ManyToManyField(JoingoTeam)
