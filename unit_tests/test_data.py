from flask_jwt_extended import create_access_token
from datetime import timedelta

def generate_test_jwt(testemail="test_user@gmail.com"):
    """Generate a test JWT for a given identity."""
    return create_access_token(identity=testemail, expires_delta=timedelta(days=30))
