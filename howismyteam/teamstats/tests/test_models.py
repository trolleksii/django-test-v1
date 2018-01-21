from django.core.exceptions import ValidationError

from teamstats.models import (
    Team, User, UserPollProfile, 
    get_happiness_stats, is_eligible_for_poll, update_poll_date
)

from .base import TeamstatsBaseTestCase


class TeamModelTest(TeamstatsBaseTestCase):

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

    def test_cant_create_team_without_name(self):
        with self.assertRaises(ValidationError):
            team = Team(name="")
            team.full_clean()


class UserPollProfileModelTest(TeamstatsBaseTestCase):

    def test_cant_create_two_profiles_for_one_user(self):
        UserPollProfile.objects.get_or_create(user=self.users[0])
        with self.assertRaises(ValidationError):
            duplicate = UserPollProfile(user=self.users[0])
            duplicate.full_clean()

    def test_cant_save_profile_without_user(self):
        with self.assertRaises(ValidationError):
            profile = UserPollProfile()
            profile.full_clean()

    def test_profile_happiness_validators(self):
        profile = UserPollProfile(user=self.users[0])
        happiness_cases = (-1, 0, 6)
        with self.assertRaises(ValidationError):
            for h in happiness_cases:
                profile.happiness = h
                profile.full_clean()


class MiscFunctionsTest(TeamstatsBaseTestCase):

    def test_get_happiness_stats_with_team(self):
        expected_detailed = [0, 0, 0, 1, 1]
        expected_average = 4.5
        team_or_none, detailed, average = get_happiness_stats(self.users[2])
        self.assertEqual(expected_average, average)
        self.assertEqual(expected_detailed, detailed)

    def test_get_happiness_stats_without_team(self):
        expected_detailed = [0, 1, 0, 0, 1]
        expected_average = 3.5
        team_or_none, detailed, average = get_happiness_stats(self.users[0])
        self.assertEqual(expected_average, average)
        self.assertEqual(expected_detailed, detailed)

    def test_eligibility_if_user_was_polled_today(self):
        expected_eligibility = False
        result = is_eligible_for_poll(self.users[0])
        self.assertEqual(result, expected_eligibility)

    def test_eligibility_if_user_was_polled_yesterday(self):
        expected_eligibility = True
        result = is_eligible_for_poll(self.users[3])
        self.assertEqual(result, expected_eligibility)

    def test_updtate_poll_time(self):
        old_date = UserPollProfile.objects.get(user=self.users[3]).poll_date
        update_poll_date(self.users[3])
        profile = UserPollProfile.objects.get(user=self.users[3])
        self.assertNotEqual(profile.poll_date, old_date)
