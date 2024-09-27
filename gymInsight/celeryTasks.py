from celery import shared_task
from emailService.sendMailService import feesRenewalNotification
from datetime import datetime
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
