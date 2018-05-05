from django.test import TestCase

from teamstats.forms import HappyUserCreationForm, UserPollForm
from teamstats.models import Team


class HappyUserCreationFormTest(TestCase):

    def test_empty_form(self):
        form = HappyUserCreationForm(data=None)
        self.assertFalse(form.is_valid())

    def test_empty_different_paswords(self):
        form_data = {
            'username': 'testuser',
            'password1': 'qwerty123',
            'password2': 'qwerty1234'
        }
        form = HappyUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_empty_team_and_new_team(self):
        team = Team.objects.create(name='Red Team')
        form_data = {
            'username': 'testuser',
            'password1': 'qwerty123',
            'password2': 'qwerty123',
            'team': team.pk,
            'add_new_team': 'Blue Team'
        }
        form = HappyUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_existing_team(self):
        team = Team.objects.create(name='Red Team')
        form_data = {
            'username': 'testuser',
            'password1': 'qwerty123',
            'password2': 'qwerty123',
            'team': team.pk
        }
        form = HappyUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_add_new_team(self):
        team_name = 'Blue Team'
        form_data = {
            'username': 'testuser',
            'password1': 'qwerty123',
            'password2': 'qwerty123',
            'add_new_team': team_name
        }
        form = HappyUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        form.save()
        _, created = Team.objects.get_or_create(name=team_name)
        self.assertFalse(created)


class UserPollFormTest(TestCase):

    def test_empty_form(self):
        form = UserPollForm(data=None)
        self.assertFalse(form.is_valid())

    def test_filled_form(self):
        form_data = {
            'happiness': 4,
        }
        form = UserPollForm(data=form_data)
        self.assertTrue(form.is_valid())
