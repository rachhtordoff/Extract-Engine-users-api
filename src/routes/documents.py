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
    file_data = request.files
    try:
        aws_service.post_document(folder_id, file_data)

    except Exception as e:
        raise ApplicationError(f"something has gone wrong with uploading documents {e}", 'unspecified')

    return {'status': 'done'}


@documents.route("/update_extraction/<folder_id>", methods=['POST'])
@jwt_required()
def update_extraction(folder_id):
    data = request.json
    try:
        ExtractionModel.update_extraction(folder_id, data)

    except Exception as e:
        raise ApplicationError(f"something has gone wrong with uploading documents {e}", 'unspecified')

    return {'status': 'done'}


@documents.route("/get_documents/<folder_id>", methods=['POST'])
def get_documents(folder_id):
    json_data = request.json

    try:
        # Ensure the request has JSON data
        if not json_data:
            return jsonify({"error": "Missing JSON data"}), 400
        doc_names = json_data
        
        # Ensure doc_names is a list
        if not isinstance(doc_names, list):
            return jsonify({"error": "doc_names should be a list"}), 400
        
        url_list = aws_service.get_documents(folder_id, doc_names)
        
        return jsonify({"urls": url_list})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
