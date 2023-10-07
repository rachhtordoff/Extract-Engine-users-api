# routes.py
from flask import request, Blueprint, jsonify
from src.exceptions import ApplicationError
from src.utilities.aws_s3 import AWSService
from src.utilities.extract_model import ExtractionModel
from flask_jwt_extended import jwt_required

documents = Blueprint('documents', __name__)
aws_service = AWSService()


@documents.route("/create_folder/<folder_id>", methods=['POST'])
@jwt_required()
def new_bucket(folder_id):
    try:
        aws_service.create_folder(folder_id)
        return jsonify({"folder_id": folder_id})

    except Exception:
        raise ApplicationError("something has gone wrong with creating an AWS folder", 'unspecified')

    return 'done'


@documents.route("/post_document/<folder_id>", methods=['POST'])
@jwt_required()
def new_document(folder_id):
    data = request.files
    try:
        aws_service.post_document(folder_id, data)
        ExtractionModel.update_extraction(folder_id, request.json)

    except Exception:
        raise ApplicationError("something has gone wrong with uploading documents", 'unspecified')

    return 'done'
