from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Team(models.Model):
    """
    Represents a team of users. Happinesuserpos stats will be calculated for all
    users of the same team.
    """
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name


class HappyTeamUser(AbstractUser):
    """
    Custom user with team and happiness level.
    """
    # User may may have a team, team can be deleted, without deleting
    # user's profile.
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    # Happiness should be null on creation of a new profile to pass the
    # eligibility check
    happiness = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )
    poll_date = models.DateField(auto_now=True)

    @property
    def is_eligible_for_poll(self):
        """
        Returns True if the user is eligible for poll (wasn't polled today).
        """
        # if happiness is not Null - user had voted before
        if self.happiness:
            # check poll date
            return self.poll_date != date.today()
        # this is the very first poll
        return True
