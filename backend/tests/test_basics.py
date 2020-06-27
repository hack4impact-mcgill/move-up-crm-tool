import unittest
from flask import current_app
from app import create_app

class BasicsTestCase(unittest.TestCase):
    # TODO Create a test database to fill with dummy data
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_landing_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Hello World!")
    
    # TODO If we revert to pagination limit for each page, test that the number of returned resources is equal to that.
    def test_mentor_get_all(self):
        response = self.client.get('/mentors/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("James Matthew" in response.get_data(as_text=True))
        self.assertTrue("Taylor Holmes" in response.get_data(as_text=True))
        self.assertTrue("Daniel Smith" in response.get_data(as_text=True))
        self.assertFalse("Hello World" in response.get_data(as_text=True))


    def test_mentor_get_by_email(self):
        response = self.client.get('/mentors/email/daniel@moveuptoday.org/')
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(len(response.data), 1) TODO 
        self.assertTrue("daniel@moveuptoday.org" in response.get_data(as_text=True))
        # self.assertEqual(response.data.email, b"daniel@moveuptoday.org") TODO
        self.assertTrue("recMHYM5rZR5MEOiW" in response.get_data(as_text=True))
        self.assertTrue("Daniel Smith" in response.get_data(as_text=True))
        self.assertFalse("Taylor Holmes" in response.get_data(as_text=True))

    def test_mentor_get_by_id(self):
        response = self.client.get('/mentors/recoRd2tV46cOjTRY/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("james@moveuptoday.org" in response.get_data(as_text=True))
        self.assertTrue("recoRd2tV46cOjTRY" in response.get_data(as_text=True))
        self.assertTrue("James Matthew" in response.get_data(as_text=True))
        self.assertFalse("Taylor Holmes" in response.get_data(as_text=True))

    def test_client_get_all(self):
        response = self.client.get('/clients/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("rec1E2HOmXx9OJFDl" in response.get_data(as_text=True))
        self.assertTrue("rec1P29DRYgv0NvEu" in response.get_data(as_text=True))
        self.assertTrue("rec1xR1ACWZ2kIZA1" in response.get_data(as_text=True))
        self.assertFalse("Do not include this data in the database" in response.get_data(as_text=True))

    def test_client_get_by_email(self):
        response = self.client.get('/clients/email/25nice.email@hotmail.com/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("25nice.email@hotmail.com" in response.get_data(as_text=True))
        self.assertTrue("rec0KxGQvEFfx693C" in response.get_data(as_text=True))
        self.assertTrue("test" in response.get_data(as_text=True))
        self.assertFalse("85nice.email@hotmail.com" in response.get_data(as_text=True))
        
    # TODO how to test attachment
    def test_client_get_by_id(self):
        response = self.client.get('/clients/rec70w2kYlVSe6RQQ/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("28nice.email@hotmail.com" in response.get_data(as_text=True))
        self.assertTrue("rec70w2kYlVSe6RQQ" in response.get_data(as_text=True))
        self.assertTrue("test" in response.get_data(as_text=True))
        self.assertFalse("85nice.email@hotmail.com" in response.get_data(as_text=True))