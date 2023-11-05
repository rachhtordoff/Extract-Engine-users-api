# aws_service.py
import boto3
from botocore.client import Config
from src import config
import io
import zipfile
import os
import shutil


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
        self.client.put_object(Bucket=config.Config.BUCKET_ID, Body='', Key=config.Config.BUCKET_NAME + '/' + folder_id)

    def post_document_extract(self, folder_id, file_data):
        for key, value in file_data.items():
            _, file_extension = os.path.splitext(key)
            if file_extension.lower() == '.zip':

                filename_without_ext = key.split('.')[0]
                extract_to = f"/opt/src/documents/{filename_without_ext}"
                file_storage = value.read()
                with io.BytesIO(file_storage) as file_like_object, zipfile.ZipFile(file_like_object, 'r') as zip_ref:
                    zip_ref.extractall(extract_to)

                for foldername, _subfolders, filenames in os.walk(extract_to):
                    for filename in filenames:
                        file_path = os.path.join(foldername, filename)
                        with open(file_path, 'rb') as file:
                            contents = file.read()
                            self.client.put_object(Bucket=config.Config.BUCKET_ID, Key=config.Config.BUCKET_NAME + f'/uploads/{folder_id}/{filename_without_ext}/{filename}', Body=contents)
                shutil.rmtree(extract_to)
            else:
                self.client.put_object(Bucket=config.Config.BUCKET_ID, Key=config.Config.BUCKET_NAME + '/uploads/' + folder_id + '/' + key, Body=value.read())
                # self.client.put_object_acl(ACL='public-read', Bucket=config.Config.BUCKET_ID, Key=config.Config.BUCKET_NAME + '/uploads/' +  folder_id + '/' + key)

    def post_document(self, folder_id, file_data):

        for key, value in file_data.items():
            self.client.put_object(Bucket=config.Config.BUCKET_ID, Key=config.Config.BUCKET_NAME + '/' + folder_id + '/' + key, Body=value.read())
            # self.client.put_object_acl(ACL='public-read', Bucket=config.Config.BUCKET_ID, Key=config.Config.BUCKET_NAME + '/' +  folder_id + '/' + key)

    def get_documents(self, doc_names):
        urls = []
        for entry in doc_names:
            for key, value in entry.items():
                url = self.client.generate_presigned_url(
                    'get_object',
                    Params={
                        'Bucket': config.Config.BUCKET_ID,
                        'Key': f"{config.Config.BUCKET_NAME}/{key}/{value}"
                    },
                    ExpiresIn=3600
                )
                urls.append({value: url})
        return urls
