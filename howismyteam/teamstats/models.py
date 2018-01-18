from datetime import date

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
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
    # Each profile must point to a user, if user is deleted, so is profile.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # User may may have a team, team can dismissed, without
    # loosing user's profile
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        related_name='teammates',
        null=True,
        blank=True
    )
    # Happiness is not mandatory on creation. It will be set from webpage.
    happiness = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )
    # Date when user was polled last time.
    # Can't set autonow, because it will prohibit user to participate the poll
    # on the day when profile was created
    # So I decided to make it optional and set explicitly during the poll.
    poll_date = models.DateField(null=True, blank=True)

    def was_polled_today(self):
        """
        Returns True if user was polled earlier this day.
        """
        return self.vote_date == date.today()

    def __str__(self):
        return self.user.username
