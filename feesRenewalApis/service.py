from rest_framework import status
from userMetaDataApis.models import UserMetaData
from userMetaDataApis.serializers import UserMetaDataSerializer
from django.utils import timezone
from emailService.sendMailService import feesRenewalNotification
from datetime import datetime
from celery import shared_task

def notifyAll(admin):
      try:
        todayDate = timezone.now().date()
        renewalUsers = UserMetaData.objects.filter(admin_id = admin['userId'], renewal_date__lte= todayDate)
        renewalUsersSerializer = UserMetaDataSerializer(renewalUsers, many = True)
        if not renewalUsersSerializer.data:
            return {"message": "No users found with upcoming renewals"}, status.HTTP_200_OK
        
        sendFeeRenewalNotification.delay(renewalUsersSerializer.data, admin)
        return {"message": "Fees renewal email send shortly to the users"},  status.HTTP_200_OK
      except UserMetaData.DoesNotExist:
           return {"error": "admin not found"}, status.HTTP_404_NOT_FOUND  
      except Exception as e:
           return {"error": "An unexpected error occured"}, status.HTTP_500_INTERNAL_SERVER_ERROR
  
        
def notifyById(admin, id):
      try:  
        userMetaData = UserMetaData.objects.get(user_id = id)
        userMetaDataSerializer = UserMetaDataSerializer(userMetaData)
        if str(userMetaDataSerializer.data.get('admin_id')) != admin['userId']:
            return {"error": "This user does not belong to your gym members or you are not authorized to send renewal notification to this user"}, status.HTTP_403_FORBIDDEN   
        
        renewalDate = datetime.strptime(userMetaDataSerializer.data['renewal_date'], "%Y-%m-%d").date()
        formattedRenewalDate = renewalDate.strftime("%d %B %Y")
        feesRenewalNotification.delay({
            "userName": f"{userMetaDataSerializer.data['user_details']['first_name']} {userMetaDataSerializer.data['user_details']['last_name']}",
            "adminName": f"{admin['firstName']} {admin['lastName']}",
            "renewalDate": formattedRenewalDate,
            "email": userMetaDataSerializer.data['user_details']['email']
        })
        return {"message": "Fees renewal email send shortly to the user"},  status.HTTP_200_OK
      except UserMetaData.DoesNotExist:
           return {"error": "user not found"}, status.HTTP_404_NOT_FOUND  
      except Exception as e:
           return {"error": "An unexpected error occured"}, status.HTTP_500_INTERNAL_SERVER_ERROR
        



@shared_task
def sendFeeRenewalNotification(renewalUsersSerializer, admin):
    for renewalUser in renewalUsersSerializer:
        renewalDate = datetime.strptime(renewalUser['renewal_date'], "%Y-%m-%d").date()
        formattedRenewalDate = renewalDate.strftime("%d %B %Y")
        feesRenewalNotification({
            "userName": f"{renewalUser['user_details']['first_name']} {renewalUser['user_details']['last_name']}",
            "adminName": f"{admin['firstName']} {admin['lastName']}",
            "renewalDate": formattedRenewalDate,
            "email": renewalUser['user_details']['email']
        })