import time
from .base import FunctionalTests


class IndexPageTest(FunctionalTests):
    """
    Simple test to check if django is working properly.
    """
    def test_django_landing_page(self):
        # Project is still empty, but Django landing page should be available
        self.browser.get('http://localhost:8000')
        self.assertIn('How is my team?', self.browser.title)
        time.sleep(10)
