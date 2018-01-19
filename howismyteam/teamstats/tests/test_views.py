from django.test import TestCase
from django.urls import reverse

from teamstats.models import User


class LoginViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testclient', password='password')

    def test_index_view_use_correct_template(self):
        response = self.client.get(reverse('index_view'))
        self.assertTemplateUsed(response, 'index.html')

    def test_successfull_login_redirects_to_result(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('teamstats:login_view'))
        self.assertRedirects(response, reverse('teamstats:results_view'))


class LogoutViewTest(TestCase):

    def test_logout_redirects_to_index_page(self):
        response = self.client.get(reverse('teamstats:logout_view'))
        self.assertRedirects(response, '/')


class ResultsViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testclient', password='password')

    def test_results_not_available_if_not_logged_in(self):
        results_url = reverse('teamstats:results_view')
        login_url = reverse('teamstats:login_view')
        response = self.client.get(results_url)
        self.assertRedirects(response, login_url+'?next='+results_url)

    def test_results_view_use_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('teamstats:results_view'))
        self.assertTemplateUsed(response, 'results.html')
        self.client.logout()
