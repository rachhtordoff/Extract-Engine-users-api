# aws_service.py
import boto3
from botocore.client import Config
from src import config


class AWSService:
    def __init__(self):
        self.client = boto3.client(
            's3',
            aws_access_key_id=config.Config.aws_access_key_id,
            aws_secret_access_key=config.Config.aws_secret_access_key,
            config=Config(signature_version='s3v4'),
            region_name='eu-west-2'
        )

    def create_folder(self, folder_id):
        self.client.put_object(Bucket=config.Config.BUCKET_ID, Body='', Key=config.Config.BUCKET_NAME + 'users/' + folder_id)

    def post_document(self, folder_id, file_data):
        for key, value in file_data.items():
            self.client.put_object(Bucket=config.Config.BUCKET_ID, Key=config.Config.BUCKET_NAME + 'users/' + folder_id + '/' + key, Body=value.read(), ServerSideEncryption="aws:kms")
