from rest_framework import status
from . models  import User
from emailService.sendMailService import sendUserCreateNotification
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from .serializers import UserSerializer
def createUser(payload):
    if payload is None:
        return {"error":"Data is missing"}, status.HTTP_400_BAD_REQUEST
    try:
        user= UserSerializer(data=dtoToModel(payload))
        if user.is_valid():
            user.save()
            sendUserCreateNotification({
                "first_name": user.data["first_name"],
                "last_name": user.data["last_name"],
                "email": user.data["email"],
                "password": payload.get("password"),
            })
            return {"user":modelToDto(user.data)},status.HTTP_201_CREATED
        else:
            return{"error": user.errors},status.HTTP_400_BAD_REQUEST

    except ValidationError as e:
        return {"error": str(e)}, status.HTTP_400_BAD_REQUEST

    except Exception as e:
        return {"error": "An unexpected error occurred"}, status.HTTP_500_INTERNAL_SERVER_ERROR

def getAllUsers():
    try:
        users= User.objects.filter(role="USER").order_by('-created_at')
        users_serialized= UserSerializer(users, many =True)
        users_dto =[]
        for user in users_serialized.data:
            users_dto.append(modelToDto(user))

        return {"users":users_dto}, status.HTTP_200_OK
    except ValidationError as e:
        return {"error": str(e)}, status.HTTP_400_BAD_REQUEST

    except Exception as e:
        return {"error": "An unexpected error occurred"}, status.HTTP_500_INTERNAL_SERVER_ERROR
    
def getById(id):
    try:
        user = User.objects.get(user_id= id)
        userSerialized = UserSerializer(user)
        return {"user": modelToDto(userSerialized.data)}, status.HTTP_200_OK
    except User.DoesNotExist as e:
        return {"error": "User not found"}, status.HTTP_404_NOT_FOUND
    except Exception as e:
        return {"error": "An unexpected error occurred"}, status.HTTP_500_INTERNAL_SERVER_ERROR

    
def update(id, payload):
    if payload is None:
        return {"error":"Data is missing"}, status.HTTP_400_BAD_REQUEST
    if payload.get('password') is not None:
        payload.pop('password')
    try:
        user = User.objects.get(user_id= id)
        updateUser = UserSerializer(user, data= updateDtoToModel(payload), partial= True)
        if updateUser.is_valid():
            updateUser.save()
            return {"user":modelToDto(updateUser.data)},status.HTTP_201_CREATED
        else:
            return{"error": updateUser.errors},status.HTTP_400_BAD_REQUEST

    except User.DoesNotExist as e:
        return {"error": "User not found"}, status.HTTP_404_NOT_FOUND

    except Exception as e:
        return {"error": "An unexpected error occurred"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            

def delete(id):
    try:
        user = User.objects.get(user_id=id)
        user.delete()
        return {"message": "User deleted successfully"}, status.HTTP_200_OK
    except User.DoesNotExist:
        return {"error": "User not found"}, status.HTTP_404_NOT_FOUND
    except Exception as e:
        return {"error": "An unexpected error occurred"}, status.HTTP_500_INTERNAL_SERVER_ERROR

def changePassword(id, payload):
    if payload is None:
        return {"error":"Data is missing"}, status.HTTP_400_BAD_REQUEST
    try:
        user= User.objects.get(user_id = id)
        userSerialized = UserSerializer(user)
        if check_password(payload.get('oldPassword'), userSerialized.data.get('password')):
            updatePassword= UserSerializer(user, data={"password":payload.get('newPassword')}, partial= True)
            if updatePassword.is_valid():
                updatePassword.save()
                return {"message":"Password Change Successfully"},status.HTTP_200_OK
            else:
                return{"error": updatePassword.errors},status.HTTP_400_BAD_REQUEST
        else:
             return{"error": "Old password is incorrect"},status.HTTP_400_BAD_REQUEST   
        
    except User.DoesNotExist:
        return {"error": "User not found"}, status.HTTP_404_NOT_FOUND    

    except ValidationError as e:
        return {"error": str(e)}, status.HTTP_400_BAD_REQUEST

    except Exception as e:
        return {"error": "An unexpected error occurred"}, status.HTTP_500_INTERNAL_SERVER_ERROR

def dtoToModel(payload):
    required_fields = ['firstName', 'lastName', 'email', 'password']
    for field in required_fields:
        if not payload.get(field):
            raise ValueError(f"Missing required field: {field}")

    return {
        "first_name": payload.get('firstName'),
        "last_name": payload.get('lastName'),
        "email": payload.get('email').lower() if payload.get('email') else None,
        "password": payload.get('password'),
        "role": "USER"
    }

def modelToDto(data):
    return {
        "userId": data.get('user_id'),
        "firstName": data.get('first_name'),
        "lastName": data.get('last_name'),
        "email": data.get('email'),
        "role": data.get('role'),
        "createdAt": data.get('created_at'),
        "updatedAt": data.get('updated_at'),
    }

def updateDtoToModel(payload):
    structuredData={}
    if payload.get('firstName'):
        structuredData['first_name'] = payload.get('firstName')
    if payload.get('lastName'):
        structuredData['last_name'] = payload.get('lastName')
    if payload.get('email'):
        structuredData['email'] = payload.get('email').lower()
    if payload.get('password'):
        structuredData['password'] = payload.get('password')

    return structuredData    