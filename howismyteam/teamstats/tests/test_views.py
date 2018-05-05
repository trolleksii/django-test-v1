from datetime import date
from django.test import TestCase
from django.urls import reverse

from teamstats.models import HappyTeamUser


class TestWithFixtures(TestCase):

    fixtures = ['profiles.json']


class IndexViewTest(TestWithFixtures):

    def test_index_view_use_correct_template(self):
        response = self.client.get(reverse('index_view'))
        self.assertTemplateUsed(response, 'index.html')


class RegistrationViewTest(TestCase):

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('teamstats:register_view'))
        self.assertTemplateUsed(response, 'register.html')

    def test_successfull_registration_redirects_to_poll(self):
        response = self.client.post(
            reverse('teamstats:register_view'),
            data={
                'username': 'testuser',
                'password1': 'qwerty123',
                'password2': 'qwerty123'
            }
        )
        self.assertRedirects(response, reverse('teamstats:userpoll_view'))

    def test_unvalid_form(self):
        response = self.client.post(
            reverse('teamstats:register_view'),
            data={
                'username': 'testuser',
                'password1': 'qwerty123',
                'password2': 'qwerty124'
            },
            follow=True
        )
        self.assertTemplateUsed(response, 'register.html')


class LoginViewTest(TestWithFixtures):

    def test_login_view_use_correct_template(self):
        response = self.client.get(reverse('teamstats:login_view'))
        self.assertTemplateUsed(response, 'login.html')

    def test_unauthenticated_users_always_redirected_to_login_page(self):
        login_url = reverse('teamstats:login_view')
        poll_url = reverse('teamstats:userpoll_view')
        results_url = reverse('teamstats:results_view')
        response = self.client.get(results_url)
        self.assertRedirects(response, login_url + '?next=' + results_url)
        response = self.client.get(poll_url)
        self.assertRedirects(response, login_url + '?next=' + poll_url)

    def test_successfull_login_redirects_to_poll(self):
        response = self.client.post(
            reverse('teamstats:login_view'),
            data={'username': 'Kenneth', 'password': 'qwerty123'}, follow=True
        )
        self.assertRedirects(response, reverse('teamstats:userpoll_view'))

    def test_successfull_login_redirects_to_results(self):
        user = HappyTeamUser.objects.get(username='Kenneth')
        user.happiness = 5
        user.save()
        response = self.client.post(
            reverse('teamstats:login_view'),
            data={'username': 'Kenneth', 'password': 'qwerty123'}, follow=True
        )
        self.assertRedirects(response, reverse('teamstats:results_view'))


class LogoutViewTest(TestCase):

    def test_logout_redirects_to_index_page(self):
        response = self.client.get(reverse('teamstats:logout_view'))
        self.assertRedirects(response, '/')


class ResultsViewTest(TestWithFixtures):

    def test_results_view_use_correct_template(self):
        # admin is always forwarded directly to results
        self.client.login(username='admin', password='qwerty123')
        response = self.client.get(reverse('teamstats:results_view'))
        self.assertTemplateUsed(response, 'results.html')

    def test_user_eligible_to_poll_cant_view_results(self):
        self.client.login(username='Kenneth', password='qwerty123')
        response = self.client.get(reverse('teamstats:results_view'))
        self.assertRedirects(response, reverse('teamstats:userpoll_view'))

    def test_user_see_team_results_only(self):
        # these teams are hardcoded in fixtures
        team1 = ('Kenneth', 'qwerty123', 5), ('Kyle', 'qwerty123', 4),
        team2 = ('Eric', 'qwerty123', 1),
        # poll everyone
        for entry in team1 + team2:
            self.client.login(username=entry[0], password=entry[1])
            self.client.post(
                reverse('teamstats:userpoll_view'),
                data={'happiness': entry[2]}
            )
            self.client.logout()
        # check votes count
        self.client.login(username='Kenneth', password='qwerty123')
        response = self.client.get(reverse('teamstats:results_view'))
        vote_count = sum([x['value'] for x in response.context['detailed']])
        self.assertEqual(vote_count, len(team1))


class PollViewTest(TestWithFixtures):

    def test_poll_view_uses_correct_template(self):
        self.client.login(username='Kenneth', password='qwerty123')
        response = self.client.get(reverse('teamstats:userpoll_view'))
        self.assertTemplateUsed(response, 'poll.html')

    def test_poll_updates_profile(self):
        self.client.login(username='Kenneth', password='qwerty123')
        self.client.post(
            reverse('teamstats:userpoll_view'),
            data={'happiness': 1}
        )
        user = HappyTeamUser.objects.get(username='Kenneth')
        self.assertEqual(user.happiness, 1)
        self.assertEqual(user.poll_date, date.today())

    def test_successfull_poll_redirects_to_results(self):
        self.client.login(username='Kenneth', password='qwerty123')
        response = self.client.post(
            reverse('teamstats:userpoll_view'),
            data={'happiness': 1}
        )
        self.assertRedirects(response, reverse('teamstats:results_view'))

    def test_user_cant_vote_twice_a_day(self):
        self.client.login(username='Kenneth', password='qwerty123')
        # sending post with happiness=3
        self.client.post(
            reverse('teamstats:userpoll_view'),
            data={'happiness': 3}
        )
        user = HappyTeamUser.objects.get(username='Kenneth')
        # happiness=3 saved to DB
        self.assertEqual(user.happiness, 3)
        # sending another post happiness=1
        self.client.post(
            reverse('teamstats:userpoll_view'),
            data={'happiness': 1}, follow=True
        )
        # happiness=1 wasn't saved to DB
        self.assertNotEqual(user.happiness, 1)
        # happiness is still 3
        self.assertEqual(user.happiness, 3)

    def test_user_cant_be_polled_without_data(self):
        self.client.login(username='Kenneth', password='qwerty123')
        response = self.client.post(
            reverse('teamstats:userpoll_view'),
            data={}, follow=True
        )
        self.assertTemplateUsed(response, 'poll.html')
