from flask import Blueprint, jsonify, request
from src.models import User
from flask_jwt_extended import create_access_token, jwt_required, create_refresh_token
from src import app, db
from datetime import timedelta

user = Blueprint('users', __name__)

@user.route('/register', methods=['POST'])
def register():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user:
        return jsonify({"message": "email taken"}), 400

    new_user = User(**data)
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created!"}), 201


@user.route('/update', methods=['PUT'])
def update_user():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Here, you can update any fields you want. For example, updating the name:
    if 'code' in data:
        user.code = data['code']
        timestamp = datetime.datetime.now()
        user.timestamp = timestamp

    db.session.commit()
    
    return jsonify({"message": "User updated successfully!"}), 200


@user.route('/update_pass', methods=['PUT'])
def update_pass():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Here, you can update any fields you want. For example, updating the name:
    
    if 'code' in data:
        if user.code == data['code']:
            # Update password if it's provided in the data
            timestamp = datetime.datetime.now()
            if timestamp < result.user + timedelta(days=10):
                if 'password' in data:
                    user.set_password(data['password'])
                    user.code = ''
                    db.session.commit()
            else:
                return jsonify({"message": "Code expired"}), 404
        else:
            return jsonify({"message": "Invalid code"}), 404
    else:
        return jsonify({"message": "Code not sent"}), 404
  
    
    return jsonify({"message": "User updated successfully!"}), 200


@user.route('/token/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user, expires_delta=timedelta(days=30))
    return jsonify(access_token=access_token), 200

@user.route('/login', methods=['POST'])
def login():
    data = request.json

    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):

        token = create_access_token(identity=user.email, expires_delta=timedelta(days=30))
        refresh_token = create_refresh_token(identity=user.email, expires_delta=timedelta(days=365))

        return jsonify(
            access_token=token,
            refresh_token=refresh_token,
            user_id=user.id, 
            name=user.fullname, 
            email=user.email
        ), 200
    return jsonify({"message": "Invalid credentials"}), 401

@user.route('/protected', methods=['GET'])
@jwt_required()
def protected_route():
    return jsonify({"message": "This is a protected route!"})

