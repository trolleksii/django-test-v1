from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    """
    Users can belong to a team. Nothing special here.
    """
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name


class UserPollProfile(models.Model):
    """
    Each user should have a profile to be able to participate in the poll.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    # TODO
    # happiness and date of last vote
