from django.test import TestCase
from django.core.exceptions import ValidationError

from teamstats.models import Team, User, UserPollProfile


class TeamModelTest(TestCase):

    def test_cant_have_duplicate_teams(self):
        Team.objects.create(name="RedTeam")
        with self.assertRaises(ValidationError):
            duplicate = Team(name="RedTeam")
            duplicate.full_clean()

    def test_can_delete_list_without_affecting_user_profile(self):
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
