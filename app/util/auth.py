
from jose import jwt 
import jose 
from datetime import datetime, timedelta, timezone


SECRET_KEY =  "super secret secrets"

def encode_token(runner_id, role):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=1),
        'iat': datetime.now(timezone.utc),
        'sub': str(runner_id), #need to convert to string or I will get an invalid token error when I try to decode
        'role': role
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256') #encoding the token
    return token