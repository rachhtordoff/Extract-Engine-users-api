from flask import request, Blueprint, Response, jsonify
from src.exceptions import ApplicationError
import json
from src import config
import boto3
from botocore.client import Config
import os
import re
from src.models import Extractions


boto3
client = boto3.client('s3',
    aws_access_key_id= config.aws_access_key_id,
    aws_secret_access_key= config.aws_secret_access_key,
    config=Config(signature_version='s3v4'),
    region_name='eu-west-2')

# This is the blueprint object that gets registered into the app in blueprints.py.
documents = Blueprint('documents', __name__)

# This is the blueprint object that gets registered into the app in blueprints.py.
@documents.route("/create_folder/<folder_id>", methods=['POST'])
def new_bucket(folder_id):
    try:

        send = client.put_object(Bucket= config.BUCKET_ID , Body='', Key=config.BUCKET_NAME + 'users/' + folder_id)
    except Exception as e:
        raise ApplicationError("something has gone wrong with creating an AWS folder", 'unspecified')
    else:

        return jsonify({
            "folder_id":folder_id
        })


#this posts documents to amazon s3 folder
@documents.route("/post_document/<folder_id>/<user_id>/<id>", methods=['POST'])
def new_document(folder_id, user_id):
    data = request.files
    try:
        for key, value in data.items():
            client.put_object(Bucket=config.BUCKET_ID, Key=config.BUCKET_NAME + 'users/' + folder_id + '/' + key, Body=value.read(), ServerSideEncryption="aws:kms")
        
            update_extraction={}
            update_extraction['output_document_name']= key

            updating = db.session.query(Extractions).get(id)
            for key, value in update_extraction.items():
                setattr(updating, key, value)
            db.session.commit()

    except Exception as e:
        raise ApplicationError("something has gone wrong with uploading documents", 'unspecified')