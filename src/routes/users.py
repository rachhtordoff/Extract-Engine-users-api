from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from src.utilities.user_service import UserService, ExtractService
from src.utilities.token_service import TokenService
from flask_jwt_extended import get_jwt_identity

user = Blueprint('users', __name__)


@user.route('/register', methods=['POST'])
def register():
    data = request.json
    try:
        UserService.create_user(data)
        return jsonify({"message": "User created!"}), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@user.route('/update', methods=['PUT'])
def update_user():
    data = request.json
    try:
        UserService.update_user_code(data['email'], data['code'])
        return jsonify({"message": "User updated successfully!"}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 404


@user.route('/update_pass', methods=['PUT'])
def update_pass():
    data = request.json
    try:
        UserService.update_user_password(data['email'], data['code'], data['password'])
        return jsonify({"message": "User updated successfully!"}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 404


@user.route('/token/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify({"message": "Unable to extract user identity."}), 401

    try:
        new_access_token = TokenService.create_tokens(current_user)[0]
        if not new_access_token:
            raise ValueError("Failed to create a new token.")
        return jsonify(access_token=new_access_token), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 401
    except Exception as e:
        # Catch other unexpected errors
        return jsonify({"message": "An unexpected error occurred.", "details": str(e)}), 500


@user.route('/login', methods=['POST'])
def login():
    data = request.json
    try:
        user = UserService.validate_user(data['email'], data['password'])
        access_token, refresh_token = TokenService.create_tokens(user.email)
        return jsonify(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user.id,
            name=user.fullname,
            email=user.email
        ), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 401


@user.route('/get_document_list/<folder_id>', methods=['GET'])
def get_document_list(folder_id):
    results = UserService.get_document_names(folder_id)

    document_list = []
    for result in results:
        document_list.append({result[0]: result[1]})

    return jsonify(document_list)


@user.route('/protected', methods=['GET'])
@jwt_required()
def protected_route():
    return jsonify({"message": "This is a protected route!"})


@user.route('/new_extract', methods=['POST'])
def new_extract():
    data = request.json
    try:
        get_extract = ExtractService.create_extract(data)

        if isinstance(get_extract, list):
            return jsonify([item.to_json() for item in get_extract])

        return jsonify(get_extract.to_json())
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except AttributeError as e:
        return jsonify({"message": "Attribute error occurred.", "details": str(e)}), 500
    except Exception as e:
        # Generic exception for unexpected errors
        return jsonify({"message": "An unexpected error occurred.", "details": str(e)}), 500
