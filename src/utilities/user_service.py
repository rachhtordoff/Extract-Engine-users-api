from src.models import User, db, Extractions
from datetime import datetime, timedelta


class UserService:
    @staticmethod
    def create_user(data):
        user = User.query.filter_by(email=data['email']).first()
        if user:
            raise ValueError("Email taken")
        new_user = User(**data)
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()

    @staticmethod
    def update_user_code(email, code):
        user = User.query.filter_by(email=email).first()
        if not user:
            raise ValueError("User not found")
        user.code = code
        user.timestamp = datetime.now()
        db.session.commit()

    @staticmethod
    def get_document_names(folder_id):
        variable= db.session.query(Extractions.output_document_name).filter(Extractions.user_id==folder_id).all()
        return variable

    @staticmethod
    def update_user_password(email, code, new_password):
        user = User.query.filter_by(email=email).first()
        if not user or user.code != code or datetime.now() > user.timestamp + timedelta(days=10):
            raise ValueError("Invalid or expired code")
        user.set_password(new_password)
        user.code = ''
        db.session.commit()

    @staticmethod
    def validate_user(email, password):
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            raise ValueError("Invalid credentials")
        return user

class ExtractService:
    @staticmethod
    def create_extract(data):
        new_user = Extractions(**data)
        db.session.add(new_user)
        db.session.commit()
        return ExtractService.get_extract(new_user.to_json())

    def get_extract(params):
        variable= db.session.query(Extractions).filter_by(**params).all()
        return variable
