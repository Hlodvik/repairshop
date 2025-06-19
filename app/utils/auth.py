from datetime import datetime, timedelta, timezone
from jose import jwt, exceptions
from flask import request, jsonify
from functools import wraps

SECRET_KEY = "a super secret, secret key"
ALGORITHM = "HS256"
EXPIRATION_MINUTES = 60

def encode_token(user_id):
    payload = {
        "exp": datetime.now(timezone.utc) + timedelta(minutes=EXPIRATION_MINUTES),
        "iat": datetime.now(timezone.utc),
        "sub": str(user_id)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            parts = request.headers['Authorization'].split(" ")
            if len(parts) == 2 and parts[0] == "Bearer":
                token = parts[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = data['sub']
        except exceptions.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except exceptions.JWTError:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(user_id, *args, **kwargs)

    return decorated