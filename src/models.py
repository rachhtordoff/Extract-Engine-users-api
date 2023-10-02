from src import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import ForeignKey, Boolean
import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    fullname = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    code = db.Column(db.String(40), unique=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow(),  nullable=True)

    def to_json(self):
        return {
            "id":self.id,
            "email":self.email,
            "fullname":self.fullname,
            "code":self.code,
            "timestamp":self.timestamp
        }

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Extractions(db.Model):
    __tablename__ = 'userextractions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("users.id"))
    file_Type = db.Column(db.String(60))
    extraction_type = db.Column(db.String(60))
    extracted_Data = db.Column(db.String())
    output_document_name = db.Column(db.String())

    def to_json(self):
        return {
            "id":self.id,
            "user_id":self.user_id,
            "file_Type":self.file_Type,
            "extraction_type":self.extraction_type,
            "extracted_Data":self.extracted_Data,
            "output_document_name":self.output_document_name
        }
