import jwt 
from rest_framework import status
from gymInsight.settings import JWT_KEY
from functools import wraps
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from userApis.helper import findOne
import datetime

def generateJwt(user):
    payload = {
        'userId': user['user_id'],
        'firstName': user['first_name'],
        'lastName': user['last_name'],
        'email': user['email'],
        'role': user['role'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=10)
    }
    token = jwt.encode(payload, JWT_KEY, algorithm='HS256')
    return token

def generateTokenForgetPassword(user):
    payload = {
        'userId': user['user_id'],
        'firstName': user['first_name'],
        'lastName': user['last_name'],
        'role': user['role'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    }
    token = jwt.encode(payload, JWT_KEY, algorithm='HS256')
    return token


def validateJwt(token):
        if not token:
            return {'error': 'Authorization token is missing','code': 400, 'status': False}
        try:
            if token.startswith('Bearer '):
              token = token.split(' ')[1]
            
            decoded_token = jwt.decode(token, JWT_KEY, algorithms=["HS256"])
            isUserExist = findOne(decoded_token.get('userId'))
            if isUserExist.get('status'):
                return {'user': decoded_token,'status': True}
            else:
                return isUserExist
        except ExpiredSignatureError:
            return {'error': 'Token has expired', 'code': 401, 'status': False}
        except InvalidTokenError:
            return {'error': 'Invalid token', 'code': 400, 'status': False}



