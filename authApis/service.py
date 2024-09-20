from userApis.models import User
from userApis.serializers import UserSerializer
from django.http import JsonResponse
from rest_framework import status
from . import jwt
from django.contrib.auth.hashers import check_password
from emailService import sendMailService
def login(payload):
    try :
        user = validateUser(payload)
        if user:
            token = jwt.generateJwt(user)
            return JsonResponse({'token': token}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error':"Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    except User.DoesNotExist:
        return JsonResponse({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED) 
    except Exception as error:
        return JsonResponse({"error": str(error)}, status=500)

def forgetPassword(payload):
    try:
        user = findByEmail(payload['email'])
        if user: 
            token= jwt.generateTokenForgetPassword(user)
            user['token'] = token
            response = sendMailService.passwordResetSendNotification(user)
            if(response['status']):
                return JsonResponse(response,status=status.HTTP_200_OK)
            else:
                return JsonResponse(response,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except User.DoesNotExist:
        return JsonResponse({"error": "Email id not found"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as error:
       return JsonResponse({"error": str(error)}, status=500)        

    





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


def verifyResetToken(token):
    validateToken = jwt.validateJwt(token)
    if validateToken['status']:
        return JsonResponse({"redirectUrl":f"journey-junction/reset-password?token={token}"},status=200)
    else:
        return JsonResponse(validateToken, status= validateToken['code'])

def resetPassword(payload, token):
    try:
        validateToken = jwt.validateJwt(token)
        if validateToken['status']:
            user= User.objects.get(user_id = validateToken['user']['userId'])
            updatePassword = UserSerializer(user, payload, partial = True)
            if updatePassword.is_valid():
                updatePassword.save()
                return JsonResponse({"message":"Password Reset Successfully"}, status= status.HTTP_204_NO_CONTENT)
            else:
                return JsonResponse({"errors": user.errors}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return JsonResponse(validateToken, status= validateToken['code'])
    
    except User.DoesNotExist:
        return JsonResponse({"error": "user not found"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as error:
       return JsonResponse({"error": str(error)}, status=500) 
