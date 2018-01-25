from datetime import date

from django.test import TestCase
from django.urls import reverse

from teamstats.models import User


class TestWithFixtures(TestCase):

    fixtures = ['profiles.json']


class IndexViewTest(TestWithFixtures):

    def test_index_view_use_correct_template(self):
        response = self.client.get(reverse('index_view'))
        self.assertTemplateUsed(response, 'index.html')


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
        profile = User.objects.get(username='Kenneth').pollprofile
        profile.poll_date = date.today()
        profile.save()
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
        # way too big
        def poll_user(username, password, happiness):
            self.client.login(username=username, password=password)
            self.client.post(
                reverse('teamstats:userpoll_view'),
                data={'happiness': happiness}
            )
            self.client.logout()

        def check_results(team):
            # calculate expected values
            expected_avg = float(sum([x[2] for x in team])) / len(team)
            expected_detailed = [0] * 5
            for entry in team:
                expected_detailed[entry[2] - 1] += 1
            # compare expected and real for each user
            for entry in team:
                self.client.login(username=entry[0], password=entry[1])
                response = self.client.get(reverse('teamstats:results_view'))
                self.assertEqual(response.context['detailed'], expected_detailed)
                self.assertEqual(response.context['average'], expected_avg)
                self.client.logout()

        # each row is a separate team
        team1 = ('Kenneth', 'qwerty123', 5), ('Kyle', 'qwerty123', 4), ('Stanley', 'qwerty123', 4)
        team2 = ('Eric', 'qwerty123', 1),
        no_team = ('Timmy', 'qwerty123', 5), ('Jimmy', 'qwerty123', 4),
        # poll everyone
        for entry in team1 + team2 + no_team:
            poll_user(
                username=entry[0],
                password=entry[1],
                happiness=entry[2]
            )
        check_results(team1)
        check_results(team2)
        check_results(no_team)


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
        profile = User.objects.get(username='Kenneth').pollprofile
        self.assertEqual(profile.happiness, 1)
        self.assertEqual(profile.poll_date, date.today())

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
        profile = User.objects.get(username='Kenneth').pollprofile
        # happiness=3 saved to DB
        self.assertEqual(profile.happiness, 3)
        # sending another post happiness=1
        self.client.post(
            reverse('teamstats:userpoll_view'),
            data={'happiness': 1}, follow=True
        )
        # happiness=1 wasn't saved to DB
        self.assertNotEqual(profile.happiness, 1)
        # happiness is still 3
        self.assertEqual(profile.happiness, 3)

    def test_user_cant_be_polled_without_data(self):
        self.client.login(username='Kenneth', password='qwerty123')
        response = self.client.post(
            reverse('teamstats:userpoll_view'),
            data={}, follow=True
        )
        self.assertTemplateUsed(response, 'poll.html')
