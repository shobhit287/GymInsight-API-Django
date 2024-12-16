from rest_framework import status
from .models import UserMetaData
from . serializers import UserMetaDataSerializer
from userApis.serializers import UserSerializer
from userApis.models import User
from emailService import sendMailService
def create(payload, admin):
    if not payload: 
        return {"error":"Data is missing"}, status.HTTP_400_BAD_REQUEST
    try:
        structuredData = dtoToModel(payload)
        structuredData['admin_id'] = admin['userId']
        userMetaSerializer = UserMetaDataSerializer(data= structuredData)
        if userMetaSerializer.is_valid():
            userMetaSerializer.save()
            return {"userMetaData": modelToDto(userMetaSerializer.data)}, status.HTTP_201_CREATED
        else:
            return {"error": userMetaSerializer.errors}, status.HTTP_400_BAD_REQUEST
    except Exception as e:
        return {"error":"An Unexpected Error Occured"}, status.HTTP_500_INTERNAL_SERVER_ERROR    


def getAll(admin):
    try:
        usersMetaData= UserMetaData.objects.filter(admin_id = admin["userId"]).order_by('-updated_at')
        userMetaDataSerializer = UserMetaDataSerializer(usersMetaData, many = True)
        structuredData = []
        for meta in userMetaDataSerializer.data:
            structuredData.append(modelToDto(meta))

        return {"usersMetaData":structuredData}, status.HTTP_200_OK
    except Exception as e:
        return {"error":"An Unexpected Error Occured"}, status.HTTP_500_INTERNAL_SERVER_ERROR    

def getById(id):
    try:
        userMetaData = UserMetaData.objects.get(user_id = id)
        userMetaDataSerializer = UserMetaDataSerializer(userMetaData)
        return {"userMetaData": modelToDto(userMetaDataSerializer.data)}, status.HTTP_200_OK
    except UserMetaData.DoesNotExist:
        return {"error": "user meta data not found"}, status.HTTP_404_NOT_FOUND
    except Exception as e:
        return {"error":"An unexpected error occured"}, status.HTTP_500_INTERNAL_SERVER_ERROR

def update(admin, id, payload):
    try:
        userMetaData = UserMetaData.objects.get(user_id = id)
        userMetaDataSerializer = UserMetaDataSerializer(userMetaData)
        if str(userMetaDataSerializer.data.get('admin_id')) != admin['userId']:
            return {"error": "This user does not belong to your gym members or you are not authorized to update their details"}, status.HTTP_403_FORBIDDEN
        updateMetaDataSerializer = UserMetaDataSerializer(userMetaData, data= updateDtoToModel(payload), partial = True)
        if updateMetaDataSerializer.is_valid():
            updateMetaDataSerializer.save()
            return {"userMetaData": modelToDto(updateMetaDataSerializer.data)}, status.HTTP_200_OK
        else :
            return {"error": updateMetaDataSerializer.errors}, status.HTTP_400_BAD_REQUEST
    except UserMetaData.DoesNotExist:
        return {"error": "user meta data not found"}, status.HTTP_404_NOT_FOUND
    except Exception as e:
        return {"error":"An unexpected error occured"}, status.HTTP_500_INTERNAL_SERVER_ERROR

def delete(admin,id):
    try:
        userMetaData = UserMetaData.objects.get(user_id = id)
        userMetaDataSerializer = UserMetaDataSerializer(userMetaData)
        if str(userMetaDataSerializer.data.get('admin_id')) != admin['userId']:
            return {"error": "This user does not belong to your gym members or you are not authorized to delete this user"}, status.HTTP_403_FORBIDDEN   
        
        user = User.objects.get(user_id= id)
        user.delete()
        return {"message": "user deleted successfully"}, status.HTTP_200_OK
    except UserMetaData.DoesNotExist or User.DoesNotExist:
        return {"error": "user meta data or user not found"}, status.HTTP_404_NOT_FOUND
    except Exception as e:
        return {"error":"An unexpected error occured"}, status.HTTP_500_INTERNAL_SERVER_ERROR


def requestPlan(user, data):
    try:
        user_obj = UserMetaData.objects.get(user_id=user["userId"])
        userDetails = UserMetaDataSerializer(user_obj)
        admin_obj = User.objects.get(user_id= userDetails.data['admin_id'])
        adminDetails = UserSerializer(admin_obj)
        sendMailService.requestPlan.delay({
            "userName": f"{user['firstName']} {user['lastName']}",
            "adminName":f"{adminDetails.data['first_name']} {adminDetails.data['last_name']}",
            "email": adminDetails.data["email"],
            "currentWeight": data['currentWeight'],
            "goalWeight": data['goalWeight'],
            "height": data.get("height"),
            "isExerciseSchedule": data.get('isExerciseSchedule'),
            "isDiet": data["isDiet"]
        })

        return {"message": "Details sent to your gym owner. You will receive a response via email soon."}, status.HTTP_200_OK
        
    except UserMetaData.DoesNotExist:
        return {"error": "User not found"}, status.HTTP_404_NOT_FOUND
    except Exception as e:
        return {"error": "An unexpected error occurred"}, status.HTTP_500_INTERNAL_SERVER_ERROR

         
    
def dtoToModel(payload):
    return {
        "user_id": payload.get('userId'),
        "trainer_assigned_name": payload.get('trainerName'),
        "shift": payload.get('shift'),
        "last_fees_submission_date": payload.get('lastFeesDate'),
        "renewal_date": payload.get('renewalDate'),
        "current_plan_months": payload.get('currentPlanDuration'),
        "payment_method": payload.get('paymentMethod'),
        "fees": payload.get('fees'),
    }

def updateDtoToModel(payload):
    response ={}
    if payload.get('trainerName'):
        response["trainer_assigned_name"]= payload.get('trainerName')

    if payload.get('shift'):    
        response["shift"]= payload.get('shift')

    if payload.get('lastFeesDate'):    
        response["last_fees_submission_date"]= payload.get('lastFeesDate')

    if payload.get('renewalDate'):
        response["renewal_date"]= payload.get('renewalDate')

    if payload.get('paymentMethod'):
        response["payment_method"]= payload.get('paymentMethod')

    if payload.get('currentPlanDuration'):
        response["current_plan_months"]= payload.get('currentPlanDuration')

    if payload.get('fees'):
        response["fees"]= payload.get('fees')
    
    return response

def modelToDto(data):
    return {
        "userMetaDataId": data.get('user_meta_data_id'),
        "userId": data.get('user_id'),
        "firstName": data['user_details']['first_name'],
        "lastName": data['user_details']['last_name'],
        "email": data['user_details']['email'],
        "trainerName": data.get('trainer_assigned_name'),
        "shift": data.get('shift'),
        "lastFeesDate": data.get('last_fees_submission_date'),
        "renewalDate": data.get('renewal_date'),
        "currentPlanDuration": data.get('current_plan_months'),
        "fees": data.get('fees'),
        "paymentMethod": data.get('payment_method'),
        "updatedAt": data.get('updated_at'),
        "createdAt": data.get('created_at'),
    }
