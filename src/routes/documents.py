# routes.py
from flask import request, Blueprint, jsonify
from src.exceptions import ApplicationError
from src.utilities.aws_s3 import AWSService
from src.utilities.extraction_model import ExtractionModel

documents = Blueprint('documents', __name__)
aws_service = AWSService()

@documents.route("/create_folder/<folder_id>", methods=['POST'])
def new_bucket(folder_id):
    try:
        aws_service.create_folder(folder_id)
        return jsonify({"folder_id": folder_id})

    except Exception as e:
        raise ApplicationError("something has gone wrong with creating an AWS folder", 'unspecified')

@documents.route("/post_document/<folder_id>/<user_id>/<id>", methods=['POST'])
def new_document(folder_id, user_id, id):
    data = request.files
    try:
        aws_service.post_document(folder_id, data)
        ExtractionModel.update_extraction(id, list(data.keys())[0])  # Assuming only one file is uploaded at a time.

    except Exception as e:
        raise ApplicationError("something has gone wrong with uploading documents", 'unspecified')
