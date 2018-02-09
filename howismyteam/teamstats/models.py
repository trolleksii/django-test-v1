from datetime import date

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinValueValidator, MaxValueValidator
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

    teammates = PollProfile.objects.filter(team=team_or_none)
    average_happiness = teammates.aggregate(Avg('happiness'))['happiness__avg']
    detailed_happiness = [teammates.filter(happiness=i).count() for i in range(1, 6)]
    return (detailed_happiness, average_happiness, )


def is_eligible_for_poll(user):
    """
    Returns True if the user is eligible for poll (wasn't polled today).
    """
    eligibility = True
    try:
        # check if happiness in not Null
        if user.pollprofile.happiness:
            # check poll date
            eligibility = user.pollprofile.poll_date != date.today()
    except ObjectDoesNotExist:
        # user don't have a poll profile, do nothing
        eligibility = False
    return eligibility


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

    def __str__(self):
        return self.user.username
