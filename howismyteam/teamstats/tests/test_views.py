from datetime import date

from django.test import TestCase
from django.urls import reverse

from teamstats.models import User, UserPollProfile

from .base import TestWithFixtures


class LoginViewTest(TestWithFixtures):

    def test_index_view_use_correct_template(self):
        response = self.client.get(reverse('index_view'))
        self.assertTemplateUsed(response, 'index.html')

    def test_successfull_login_redirects(self):
        response = self.client.post(
            reverse('teamstats:login_view'),
            data={'username': 'admin', 'password': 'qwerty123'}
        )
        self.assertRedirects(response, reverse('teamstats:results_view'))


class LogoutViewTest(TestCase):

    def test_logout_redirects_to_index_page(self):
        response = self.client.get(reverse('teamstats:logout_view'))
        self.assertRedirects(response, '/')


class ResultsViewTest(TestWithFixtures):

    def test_results_not_available_if_not_logged_in(self):
        results_url = reverse('teamstats:results_view')
        login_url = reverse('teamstats:login_view')
        response = self.client.get(results_url)
        self.assertRedirects(response, login_url + '?next=' + results_url)

    def test_results_view_use_correct_template(self):
        # admin is forwarded directly to results
        self.client.login(username='admin', password='qwerty123')
        response = self.client.get(reverse('teamstats:results_view'))
        self.assertTemplateUsed(response, 'results.html')

    def test_redirects_to_poll_if_user_eligible(self):
        self.client.login(username='Kenneth', password='qwerty123')
        response = self.client.get(reverse('teamstats:results_view'))
        self.assertRedirects(response, reverse('teamstats:userpoll_view'))


class PollViewTest(TestWithFixtures):

    def test_poll_updates_profile(self):
        self.client.login(username='Kenneth', password='qwerty123')
        response = self.client.post(
            reverse('teamstats:userpoll_view'),
            data={'happiness': 1}
        )
        self.assertRedirects(response, reverse('teamstats:results_view'))
        user = User.objects.get(username='Kenneth')
        profile = UserPollProfile.objects.get(user=user)
        self.assertEqual(profile.happiness, 1)
        self.assertEqual(profile.poll_date, date.today())

    def test_non_eligible_user(self):
        user = User.objects.get(username='Kenneth')
        profile = UserPollProfile.objects.get(user=user)
        profile.poll_date = date.today()
        profile.save()
        self.client.login(username='Kenneth', password='qwerty123')
        response = self.client.get(reverse('teamstats:userpoll_view'))
        self.assertRedirects(response, reverse('teamstats:results_view'))

    def test_poll_view_uses_correct_template(self):
        self.client.login(username='Kenneth', password='qwerty123')
        response = self.client.get(reverse('teamstats:userpoll_view'))
        self.assertTemplateUsed(response, 'poll.html')
