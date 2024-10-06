from userApis.models import User
from userApis.serializers import UserSerializer
from adminMetaDataApis.serializers import AdminDocumentDataSerializer
from django.http import JsonResponse
from rest_framework import status
from . import jwt
from django.contrib.auth.hashers import check_password
from emailService import sendMailService
from emailService.sendMailService import sendAdminUserCreateNotification
import random, string
def login(payload):
    try :
        user = validateUser(payload)
        if user:
            token = jwt.generateJwt(user)
            return {'token': token}, status.HTTP_200_OK
        else:
            return {'error':"Invalid Credentials"}, status.HTTP_401_UNAUTHORIZED

    except User.DoesNotExist:
        return {"error": "Invalid Credentials"}, status.HTTP_401_UNAUTHORIZED
    except Exception as error:
        return {"error": str(error)}, status.HTTP_500_INTERNAL_SERVER_ERROR
    
def googleAuthLogin(payload):
    try :
        validateToken = jwt.validateJwtGoogleAuth(payload.get('token'))
        if validateToken['status']:
            user = findByEmail(validateToken['user']['email'])
            if user:
                token = jwt.generateJwt(user)
                return {'token': token}, status.HTTP_200_OK
        else:
            return validateToken, validateToken['code']

    except User.DoesNotExist:
        createData = {
            "first_name": validateToken['user']['given_name'],
            "last_name": validateToken['user']['family_name'],
            "email": validateToken['user']['email'],
            "password": generateRandomPassword(),
            "role": "ADMIN"
        }
        user = UserSerializer(data= createData)
        if user.is_valid():
            user.save()
            adminDocumentSerializer = AdminDocumentDataSerializer(data= {"admin_id" : user.data['user_id']})
            if adminDocumentSerializer.is_valid():
                adminDocumentSerializer.save()
                sendAdminUserCreateNotification.delay({
                    "userName" : f"{user.data['first_name']} {user.data['last_name']}",
                    "email": user.data["email"],
                })
                token = jwt.generateJwt(user.data)
                return {'token': token}, status.HTTP_200_OK
            else:
                return{"error": adminDocumentSerializer.errors},status.HTTP_500_INTERNAL_SERVER_ERROR   
        else: 
            return {'error': user.errors}, status.HTTP_500_INTERNAL_SERVER_ERROR
        
    except Exception as error:
        return {"error": str(error)}, status.HTTP_500_INTERNAL_SERVER_ERROR

def forgetPassword(payload):
    try:
        user = findByEmail(payload['email'])
        if user: 
            token= jwt.generateTokenForgetPassword(user)
            user['token'] = token
            response = sendMailService.passwordResetSendNotification.delay(user)
            if(response['status']):
                return response, status.HTTP_200_OK
            else:
                return response, status.HTTP_500_INTERNAL_SERVER_ERROR

    except User.DoesNotExist:
        return {"error": "Email id not found"}, status.HTTP_401_UNAUTHORIZED
    except Exception as error:
       return {"error": str(error)}, status.HTTP_500_INTERNAL_SERVER_ERROR      

    

def findByEmail(email):
    user = User.objects.get(email = email)
    userSerializer = UserSerializer(user)
    return userSerializer.data


def validateUser(payload):
    user = findByEmail(payload['email'].lower())
    if user:
        if check_password(payload['password'], user['password']):
            return user
        return None

    

def resetPassword(payload, token):
    try:
        validateToken = jwt.validateJwt(token)
        if validateToken['status']:
            user= User.objects.get(user_id = validateToken['user']['userId'])
            updatePassword = UserSerializer(user, payload, partial = True)
            if updatePassword.is_valid():
                updatePassword.save()
                return {"message":"Password Reset Successfully"},  status.HTTP_204_NO_CONTENT
            else:
                return {"errors": user.errors}, status.HTTP_400_BAD_REQUEST

        else:
            return validateToken, validateToken['code']
    
    except User.DoesNotExist:
        return {"error": "user not found"}, status.HTTP_401_UNAUTHORIZED
    except Exception as error:
       return {"error": str(error)}, status.HTTP_500_INTERNAL_SERVER_ERROR

def generateRandomPassword(length=8):
    """Generate a random password of specified length."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))