from datetime import date, timedelta

from django.test import TestCase
from django.core.exceptions import ValidationError

from teamstats.models import (
    Team, User, UserPollProfile, 
    get_happiness_stats, is_eligible_for_poll, update_poll_date
)


class TeamModelTest(TestCase):

    def test_cant_have_duplicate_teams(self):
        Team.objects.create(name="RedTeam")
        with self.assertRaises(ValidationError):
            duplicate = Team(name="RedTeam")
            duplicate.full_clean()

    def test_can_delete_list_without_deleting_user_profile(self):
        user = User.objects.create(username="TestUser1", password="password")
        team = Team.objects.create(name="Red Team")
        UserPollProfile.objects.create(user=user, team=team)
        team.delete()
        profile = UserPollProfile.objects.get(user=user)
        self.assertEqual(profile.team, None)
        user.delete()
        profile.delete()

    def test_cant_create_team_without_name(self):
        with self.assertRaises(ValidationError):
            team = Team(name="")
            team.full_clean()


class UserPollProfileModelTest(TestCase):

    def test_cant_create_two_profiles_for_one_user(self):
        user = User.objects.create(username="TestUser1", password="password")
        UserPollProfile.objects.create(user=user)
        with self.assertRaises(ValidationError):
            duplicate = UserPollProfile(user=user)
            duplicate.full_clean()

    def test_cant_save_profile_without_user(self):
        with self.assertRaises(ValidationError):
            profile = UserPollProfile()
            profile.full_clean()

    def test_profile_happiness_validators(self):
        user = User.objects.create(username="TestUser1", password="password")
        happiness_cases = (-1, 0, 6)
        with self.assertRaises(ValidationError):
            for h in happiness_cases:
                profile = UserPollProfile(user=user, happiness=h)
                profile.full_clean()
        user.delete()


class MiscFunctionsTest(TestCase):

    def test_get_happiness_stats_with_team(self):
        user = User.objects.create(username="TestUser0", password="password")
        team = Team.objects.create(name='Red Team')
        UserPollProfile.objects.create(
            user=user,
            team=team,
            happiness=2)
        for i in range(1, 5):
            new_user = User.objects.create(
                username="TestUser{}".format(i), 
                password="password"
            )
            UserPollProfile.objects.create(user=new_user, happiness=4)
        expected_detailed = [0, 1, 0, 0, 0]
        expected_average = 2
        detailed, average = get_happiness_stats(user)
        self.assertEqual(expected_average, average)
        self.assertEqual(expected_detailed, detailed)

    def test_get_happiness_stats_without_team(self):
        user = User.objects.create(username="TestUser0", password="password")
        UserPollProfile.objects.create(user=user, happiness=1)
        for i in range(1, 5):
            new_user = User.objects.create(
                username="TestUser{}".format(i),
                password="password"
            )
            UserPollProfile.objects.create(user=new_user, happiness=5)
        expected_detailed = [1, 0, 0, 0, 4]
        expected_average = 4.2
        detailed, average = get_happiness_stats(user)
        self.assertEqual(expected_average, average)
        self.assertEqual(expected_detailed, detailed)

    def test_eligibility_if_user_was_polled_today(self):
        user = User.objects.create(username="TestUser0", password="password")
        UserPollProfile.objects.create(user=user, poll_date=date.today())
        expected = False
        result = is_eligible_for_poll(user)
        self.assertEqual(result, expected)

    def test_eligibility_if_user_was_polled_yesterday(self):
        user = User.objects.create(username="TestUser0", password="password")
        UserPollProfile.objects.create(
            user=user,
            poll_date=date.today() - timedelta(days=1)
        )
        expected = True
        result = is_eligible_for_poll(user)
        self.assertEqual(result, expected)

    def test_updtate_poll_time(self):
        user = User.objects.create(username="TestUser0", password="password")
        old_date = date.today() - timedelta(days=1)
        UserPollProfile.objects.create(
            user=user,
            poll_date=old_date
        )
        update_poll_date(user)
        profile = UserPollProfile.objects.get(user=user)
        self.assertNotEqual(profile.poll_date, old_date)
