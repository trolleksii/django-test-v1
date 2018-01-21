from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTests


class GeneralUsabilityTest(FunctionalTests):

    def test_index_page_is_available(self):
        self.browser.get(self.live_server_url)
        self.assertIn('How is my team?', self.browser.title)

    def test_login_vote_see_results_and_logout(self):
        self.browser.get(self.live_server_url)
        # logging in
        self.browser.find_element_by_id('id_main_login').click()
        self.wait_for(lambda: self.browser.find_element_by_id('id_login_form'))
        self.browser.find_element_by_id('id_username').send_keys('Kenneth')
        self.browser.find_element_by_id('id_password').send_keys('qwerty123')
        self.browser.find_element_by_id('id_password').send_keys(Keys.ENTER)
        self.wait_for(lambda: self.browser.find_element_by_id('id_happiness'))
        # participate in poll
        self.browser.find_element_by_id('id_happiness_4').send_keys(Keys.SPACE)
        self.browser.find_element_by_id('id_happiness_4').send_keys(Keys.ENTER)
        self.wait_for(lambda: self.browser.find_element_by_id('id_results_table'))
        # check if login button disappeared
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_id('id_main_login')
            self.browser.find_element_by_id('id_nav_login')
        # logging out
        self.browser.find_element_by_id('id_nav_logout').click()
        # check if log out button disappeared
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_id('id_nav_logout')

    def test_user_cant_be_polled_twice(self):
        pass

    def test_empty_form_poll(self):
        pass

    def test_users_see_only_stats_of_their_team(self):
        pass

    def test_admin_see_stats_and_navbar_href(self):
        pass
