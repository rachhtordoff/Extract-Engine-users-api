from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta


class TokenService:
    @staticmethod
    def create_tokens(user_email):
        token = create_access_token(identity=user_email, expires_delta=timedelta(days=30))
        refresh_token = create_refresh_token(identity=user_email, expires_delta=timedelta(days=365))
        return token, refresh_token
