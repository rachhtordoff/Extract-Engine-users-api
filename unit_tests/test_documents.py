import json
import unittest
from src import app
from unittest.mock import patch, ANY
from io import BytesIO
from unit_tests.test_data import generate_test_jwt


class DocumentTests(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.ctx = self.app.app_context()
        self.ctx.push()

        self.client = app.test_client()
        self.client.testing = True

    @patch('src.utilities.aws_s3.AWSService.create_folder')
    def test_create_folder(self, mock_create_folder):
        with self.app.test_client() as c, c.session_transaction() as sess:
            sess['email'] = 'john@example.com'
            sess['access_token'] = generate_test_jwt()

            folder_id = 'example_folder'
            headers = {'Authorization': f'Bearer {sess["access_token"]}'}

            response = c.post(f'/create_folder/{folder_id}', headers=headers)

            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data.decode())
            self.assertEqual(data['folder_id'], folder_id)
            mock_create_folder.assert_called_once_with(folder_id)

    @patch('src.utilities.aws_s3.AWSService.post_document')
    def test_new_document(self, mock_post_document):
        folder_id = 'example_folder'

        with self.app.test_client() as c, c.session_transaction() as sess:
            sess['email'] = 'john@example.com'
            sess['access_token'] = generate_test_jwt()

            headers = {
                'Authorization': f'Bearer {sess["access_token"]}'
            }

            data = dict(file=(BytesIO(b'my file contents'), 'test_file.pdf')) # noqa
            response = c.post(f'/post_document/{folder_id}',
                              content_type='multipart/form-data',
                              data=data, headers=headers)
            self.assertEqual(response.status_code, 200)

            # Using ANY to avoid asserting the exact object for the file
            mock_post_document.assert_called_once_with(folder_id, ANY)
