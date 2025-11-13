
from jose import jwt 
import jose 
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify

SECRET_KEY =  "super secret secrets"

def encode_token(runner_id, email):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=1),  #expiration date
        'iat': datetime.now(timezone.utc),   #issued at
        'sub': str(runner_id), #need to convert to string or I will get an invalid token error when I try to decode
        'email': email
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256') #encoding the token
    return token

def token_required(f): #wraps around a function 'f'
    @wraps(f)
    def decoration(*args, **kwargs):

        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1] # headers: {"Authorization": "Bearer my_token"}

        if not token:
            return jsonify({"error": "token missing from authorization headers"}), 401
        
        try:
            
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.runner_id = int(data['sub']) #adding the runner's id from the token to the request to be accessed in the wrapped function

        except jose.exceptions.ExpiredSignatureError:
            return jsonify({'error': 'token is expired'}), 403
        except jose.exceptions.JWTError:
            return jsonify({'error': 'invalid token'}), 403
        
        return f(*args, **kwargs)
    
    return decoration