from selenium import webdriver
from django.test import TestCase
from pyvirtualdisplay import Display

class NavFuncTest(TestCase):

    def setUp(self):
        self.display = Display(visible=0, size=(1024, 768))
        self.display.start()
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()
        self.display.stop()

    def test_initial_nav(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('J J R D Y N', self.browser.title)

if __name__ == '__main__':
    unittest.main()
