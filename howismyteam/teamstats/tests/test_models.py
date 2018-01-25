from django.core.exceptions import ValidationError
from django.test import TestCase

from teamstats.models import Team, User, PollProfile


class TeamModelTest(TestCase):

    def test_cant_have_duplicate_teams(self):
        Team.objects.create(name="RedTeam")
        with self.assertRaises(ValidationError):
            duplicate = Team(name="RedTeam")
            duplicate.full_clean()

    def test_can_delete_list_without_deleting_user_profile(self):
        user = User.objects.create(username="TestUser1", password="password")
        team = Team.objects.create(name="Red Team")
        PollProfile.objects.create(user=user, team=team)
        team.delete()
        profile = PollProfile.objects.get(user=user)
        self.assertEqual(profile.team, None)

    def test_cant_create_team_without_name(self):
        with self.assertRaises(ValidationError):
            team = Team(name="")
            team.full_clean()


class PollProfileModelTest(TestCase):

    def test_cant_create_two_profiles_for_one_user(self):
        PollProfile.objects.get_or_create(
            user=User.objects.get_or_create(username='Eric')[0]
        )
        with self.assertRaises(ValidationError):
            duplicate = PollProfile(
                user=User.objects.get_or_create(username='Eric')[0]
            )
            duplicate.full_clean()

    def test_cant_save_profile_without_user(self):
        with self.assertRaises(ValidationError):
            profile = PollProfile()
            profile.full_clean()

    def test_profile_happiness_validators(self):
        profile = PollProfile(
            user=User.objects.get_or_create(username='Eric')[0]
        )
        happiness_cases = (-1, 0, 6)
        with self.assertRaises(ValidationError):
            for h in happiness_cases:
                profile.happiness = h
                profile.full_clean()
