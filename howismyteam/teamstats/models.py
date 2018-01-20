from datetime import date

from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg


def get_happiness_stats(user):
    """
    Returns details on happines detais and an average in a tuple.
    If user is in some team, stats are calculated for this team only. In other
    case, stats are calculated for every user without a team.
    """
    try:
        team_or_none = UserPollProfile.objects.get(user=user).team
    except ObjectDoesNotExist:
        # for user without profile get stats for all users without a team
        team_or_none = None
    detailed_happiness = [UserPollProfile.objects.filter(happiness=i, team=team_or_none).count() for i in range(1, 6)]
    average_happiness = UserPollProfile.objects.filter(team=team_or_none).aggregate(Avg('happiness'))['happiness__avg']
    return (team_or_none, detailed_happiness, average_happiness, )


def is_eligible_for_poll(user):
    """
    Returns True if user wasn't polled earlier this day.
    """
    try:
        user_poll_profile = UserPollProfile.objects.get(user=user)
    except ObjectDoesNotExist:
        # for user without profile skip the poll
        return False
    return user_poll_profile.poll_date != date.today()


def update_poll_date(user):
    """
    Set today as a poll_date in UserPollProfile of a corresponding user.
    """
    profile = UserPollProfile.objects.get(user=user)
    profile.poll_date = date.today()
    profile.full_clean()
    profile.save()


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

    def __str__(self):
        return self.user.username
