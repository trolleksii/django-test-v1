from datetime import date
from functools import partial

from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg


def get_happiness_stats(user):
    """
    Returns breakdown on happines level and an average happiness as a tuple.
    If the user is in some team, stats are calculated for this team only. In
    the other case, stats are calculated for all users without a team.
    """
    try:
        team_or_none = user.pollprofile.team
    except ObjectDoesNotExist:
        # if the user is without a profile - calculate stats for all users
        # without a team
        team_or_none = None

    get_teammates = partial(PollProfile.objects.filter, team=team_or_none)
    detailed_happiness = [get_teammates(happiness=i).count() for i in range(1, 6)]
    average_happiness = get_teammates().aggregate(Avg('happiness'))['happiness__avg']
    return (detailed_happiness, average_happiness, )


def is_eligible_for_poll(user):
    """
    Returns True if the user is eligible for poll (wasn't polled today).
    """
    try:
        return user.pollprofile.poll_date != date.today()
    except ObjectDoesNotExist:
        # if the user is without a profile - skip the poll
        return False


class Team(models.Model):
    """
    Represents a team of users. Happinesuserpos stats will be calculated for all
    users of the same team.
    """
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name


class PollProfile(models.Model):
    """
    Represents user's poll profile. Each user should have a profile to be able
    to participate in the poll.
    """
    # Each profile must point to a user, if the user is deleted, so is profile.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # User may may have a team, team can be deleted, without deleting
    # user's profile.
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
    # Date when user was polled last time. Not mandatory, will be set on poll.
    poll_date = models.DateField(null=True, blank=True)

    def update_poll_date(self):
        """
        Set poll_date in PollProfile of a corresponding user for today.
        """
        self.poll_date = date.today()
        self.full_clean()
        self.save()

    def __str__(self):
        return self.user.username
