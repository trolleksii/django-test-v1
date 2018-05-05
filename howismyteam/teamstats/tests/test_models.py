from django.core.exceptions import ValidationError
from django.test import TestCase

from teamstats.models import HappyTeamUser, Team


class TeamModelTest(TestCase):

    def test_cant_have_duplicate_teams(self):
        Team.objects.create(name="RedTeam")
        with self.assertRaises(ValidationError):
            duplicate = Team(name="RedTeam")
            duplicate.full_clean()

    def test_can_delete_list_without_deleting_user_profile(self):
        user = HappyTeamUser.objects.create_user(username="TestUser1", password="password")
        team = Team.objects.create(name="Red Team")
        team.delete()
        self.assertEqual(user.team, None)

    def test_cant_create_team_without_name(self):
        with self.assertRaises(ValidationError):
            team = Team(name="")
            team.full_clean()


class HappyUserModelTest(TestCase):

    def test_happiness_validators(self):
        user = HappyTeamUser.objects.get_or_create(username='Eric')[0]
        happiness_cases = (-1, 0, 6)
        with self.assertRaises(ValidationError):
            for h in happiness_cases:
                user.happiness = h
                user.full_clean()
