import json
import unittest
from src import app
from unittest.mock import patch, ANY
from io import BytesIO


class DocumentTests(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.ctx = self.app.app_context()
        self.ctx.push()

        self.client = app.test_client()
        self.client.testing = True

    @patch('src.utilities.aws_s3.AWSService.create_folder')
    def test_create_folder(self, mock_create_folder):
        folder_id = 'example_folder'

        with self.client:
            response = self.client.post(f'/create_folder/{folder_id}')

            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data.decode())
            self.assertEqual(data['folder_id'], folder_id)
            mock_create_folder.assert_called_once_with(folder_id)

    @patch('src.utilities.aws_s3.AWSService.post_document')
    @patch('src.utilities.extract_model.ExtractionModel.update_extraction')
    def test_new_document(self, mock_update_extraction, mock_post_document):
        folder_id = 'example_folder'
        user_id = 'user1'
        id = 'doc1'

        with self.client:
            data = dict(file=(BytesIO(b'my file contents'), 'test_file.pdf')) # noqa
            response = self.client.post(f'/post_document/{folder_id}/{user_id}/{id}',
                                        content_type='multipart/form-data',
                                        data=data)

            self.assertEqual(response.status_code, 200)

            # Using ANY to avoid asserting the exact object for the file
            mock_post_document.assert_called_once_with(folder_id, ANY)
            mock_update_extraction.assert_called_once_with(id, 'file')
