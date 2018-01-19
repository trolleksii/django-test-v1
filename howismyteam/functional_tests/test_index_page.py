import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTests


class IndexPageTest(FunctionalTests):
    """
    Bunch of test to check if index page and its elements are working properly.
    """
    def test_index_page_is_available(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('How is my team?', self.browser.title)

    def test_user_can_log_in_and_out(self):
        self.browser.get('http://localhost:8000')
        # logging in
        self.browser.find_element_by_id('id_log_in').click()
        self.browser.find_element_by_id('id_username').send_keys('__testuser')
        self.browser.find_element_by_id('id_password').send_keys('qwerty123')
        self.browser.find_element_by_id('id_password').send_keys(Keys.ENTER)
        # check if log in button disappeared
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_id('id_log_in')
        # logging out
        self.browser.find_element_by_id('id_log_out').click()
        # check if log out button disappeared
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_id('id_log_out')
        # time.sleep(20)
