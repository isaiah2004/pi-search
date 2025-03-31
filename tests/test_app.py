import unittest
from src.app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_convert_and_search(self):
        response = self.app.post('/search', json={'input_string': 'hello'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('indexes', data)
        self.assertIsInstance(data['indexes'], list)

    def test_invalid_input(self):
        response = self.app.post('/search', json={'input_string': ''})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_nonexistent_word(self):
        response = self.app.post('/search', json={'input_string': 'nonexistentword'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('indexes', data)
        self.assertEqual(data['indexes'], [])

if __name__ == '__main__':
    unittest.main()