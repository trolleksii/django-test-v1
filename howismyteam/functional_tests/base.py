from selenium import webdriver

from unittest import TestCase

from teamstats.models import User, Team, UserPollProfile


class FunctionalTests(TestCase):
    """
    Base class with setUp, tearDown and other helper methods.
    """
    test_users = []

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()
