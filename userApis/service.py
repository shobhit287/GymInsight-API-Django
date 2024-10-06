from rest_framework import status
from .models  import User
from emailService.sendMailService import sendUserCreateNotification, sendAdminUserCreateNotification
from rest_framework.exceptions import ValidationError
from adminMetaDataApis.serializers import AdminDocumentDataSerializer
from django.contrib.auth.hashers import check_password
from .serializers import UserSerializer
def create(payload):
    if payload is None:
        return {"error":"Data is missing"}, status.HTTP_400_BAD_REQUEST
    try:
        user= UserSerializer(data=dtoToModel(payload))
        if user.is_valid():
            user.save()
            if user.data["role"] == "ADMIN":
                adminDocumentSerializer = AdminDocumentDataSerializer(data= {"admin_id" : user.data['user_id']})
                if adminDocumentSerializer.is_valid():
                    adminDocumentSerializer.save()
                else:
                    return{"error": adminDocumentSerializer.errors},status.HTTP_400_BAD_REQUEST    
                sendAdminUserCreateNotification.delay({
                    "userName" : f"{user.data['first_name']} {user.data['last_name']}",
                    "email": user.data["email"],
                })
            else :
                  sendUserCreateNotification.delay({
                    "userName" : f"{user.data['first_name']} {user.data['last_name']}",
                    "email": user.data["email"],
                })  
            return {"user":modelToDto(user.data)},status.HTTP_201_CREATED
        else:
            return{"error": user.errors},status.HTTP_400_BAD_REQUEST

    except ValidationError as e:
        return {"error": str(e)}, status.HTTP_400_BAD_REQUEST

    except Exception as e:
        return {"error": "An unexpected error occurred","error":e}, status.HTTP_500_INTERNAL_SERVER_ERROR

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
    return {
        "first_name": payload.get('firstName'),
        "last_name": payload.get('lastName'),
        "email": payload.get('email').lower() if payload.get('email') else None,
        "password": payload.get('password'),
        "role": payload.get('role')
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
    if payload.get('role'):
        structuredData['role'] = payload.get('role')

    return structuredData    