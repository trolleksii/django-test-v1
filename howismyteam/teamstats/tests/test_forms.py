from django.test import TestCase

from teamstats.forms import UserPollForm


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
