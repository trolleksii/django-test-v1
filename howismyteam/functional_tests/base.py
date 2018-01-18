from selenium import webdriver

from unittest import TestCase


class FunctionalTests(TestCase):
    """
    Base class with setUp, tearDown and other helper methods.
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()
