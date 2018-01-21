import time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

MAX_WAIT = 10


class FunctionalTests(StaticLiveServerTestCase):
    """
    Base class with setUp, tearDown and other helper methods.
    """
    fixtures = ['profiles.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def wait_for(self, waited_fn):
        start_time = time.time()
        while True:
            try:
                return waited_fn()
            except (AssertionError, WebDriverException) as err:
                if time.time() - start_time > MAX_WAIT:
                    raise err
                time.sleep(0.5)
