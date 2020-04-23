import os
import unittest
from briscola import flask_briscola
 
class BasicTests(unittest.TestCase):
 
    ############################
    #### setup and teardown ####
    ############################
 
    # executed prior to each test
    def setUp(self):
        flask_briscola.app.config['TESTING'] = True
        flask_briscola.app.config['WTF_CSRF_ENABLED'] = False
        flask_briscola.app.config['DEBUG'] = False
        self.app = flask_briscola.app.test_client()
 
 
    # executed after each test
    def tearDown(self):
        pass
 
 
###############
#### tests ####
###############
 
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
 
 
if __name__ == "__main__":
    unittest.main()