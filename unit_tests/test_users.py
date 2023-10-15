import json
import unittest
from src import app
from src.utilities.user_service import UserService
from unittest.mock import patch


class UserTests(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.ctx = self.app.app_context()
        self.ctx.push()

        self.client = app.test_client()
        self.client.testing = True

    def test_register_user(self):
        with self.client:
            response = self.client.post('/register',
                                        data=json.dumps({"email": "test@example.com", 'fullname': 'usernametest',
                                                         "password": "testpass"}),
                                        content_type='application/json')
            self.assertEqual(response.status_code, 201)
            data = json.loads(response.data.decode())
            print(response.text)
            print(data)
            self.assertIn("User created!", data["message"])


    @patch.object(UserService, 'create_user')
    def test_register_user_with_mock(self, mock_create_user):
        mock_create_user.return_value = None

        with self.client as c:
            with c.session_transaction() as sess:
                sess['email'] = 'john@example.com'
                sess['access_token'] = 'dummy_access_token'

                response = c.post('/register',
                                            data=json.dumps({"email": "test@example.com", "password": "testpass",
                                                            'fullname': 'usernametest'}),
                                            content_type='application/json')
                self.assertEqual(response.status_code, 201)
                data = json.loads(response.data.decode())
                self.assertIn("User created!", data["message"])
