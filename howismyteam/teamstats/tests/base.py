from datetime import date, timedelta

from django.test import TestCase

from teamstats.models import (
    User, UserPollProfile, Team,
)


class ViewBaseTestCase(TestCase):

    credentials = [
        {
            'username': 'User1',
            'password': 'password',
            'happiness': 2,
            'poll_date': date.today(),
        },
        {
            'username': 'User2',
            'password': 'password',
            'happiness': 5,
        },
        {
            'username': 'User3',
            'password': 'password',
            'team': 'SomeTeam',
            'happiness': 5,
        },
        {
            'username': 'User4',
            'password': 'password',
            'team': 'SomeTeam',
            'happiness': 4,
            'poll_date': date.today() - timedelta(days=1),
        }
    ]

    @classmethod
    def setUpTestData(cls):
        cls.users = create_test_users(cls.credentials)


def create_test_users(data):
    """
    Tekes tuple of dictionaries with credentials for user profiles and returns
    set of users that were added to the DB.
    """
    users = []
    for entry in data:
        kw = {}
        kw['user'] = User.objects.create(
            username=entry['username'],
            password=entry['password']
        )
        users.append(kw['user'])
        team = entry.get('team', False)
        happiness = entry.get('happiness', False)
        poll_date = entry.get('poll_date', False)
        if team:
            kw['team'] = Team.objects.get_or_create(name=team)[0]
        if happiness:
            kw['happiness'] = happiness
        if poll_date:
            kw['poll_date'] = poll_date
        UserPollProfile.objects.create(**kw)
    return users
