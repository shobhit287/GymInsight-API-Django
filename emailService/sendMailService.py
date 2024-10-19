import os
from dotenv import load_dotenv
from celery import shared_task
from .emailTemplateConfig import emailTemplateConfigs
from .sendEmail import sendEmailNotification
load_dotenv()

@shared_task
def passwordResetSendNotification(data):
    dynamicData= {
                  "userName" : f"{data['first_name']} {data['last_name']}",
                  "email":data['email'],
                  "link" : f"{os.getenv('BASE_URL')}/verify-token?token={data['token']}",
                  "subject": 'Password Reset Request'
                }
    response = sendEmailNotification(dynamicData, emailTemplateConfigs['PASSWORD_RESET_TEMPLATE'])
    if response['status']:
        print(f"password reset email send successfully to {dynamicData['email']}")
        return {'message': 'Reset link sent to your mail', "status": True}
    else: 
        return response

@shared_task   
def sendAdminUserCreateNotification(data):
    data["link"] = f"{os.getenv('BASE_URL')}/login"
    data["subject"] = 'Welcome to Gym Insight!'
    response = sendEmailNotification(data, emailTemplateConfigs['ADMIN_CREDENTIALS_TEMPLATE'])
    if response['status']:
        print(f"admin credentials  send successfully to {data['email']}")

@shared_task
def sendUserCreateNotification(data):
    data["link"] = f"{os.getenv('BASE_URL')}/login"
    data["subject"] = 'Gym Insight User Credentials'
    response = sendEmailNotification(data, emailTemplateConfigs['USER_CREDENTIALS_TEMPLATE'])
    if response['status']:
        print(f"user credentials  send successfully to {data['email']}")

@shared_task
def documentApprovalRejectNotification(data):
    data['link'] = f"{os.getenv('BASE_URL')}/gym-owners?adminId={data['id']}"
    data['subject'] = 'Gym Insight - Gym Details Verification'
    response = sendEmailNotification(data, emailTemplateConfigs['DOCUMENT_APPROVAL_REJECT'])
    if response['status']:
        print(f"Gym details send successfully to super admin")

@shared_task
def updatedDocumentApprovalRejectNotification(data):
    data['link'] = f"{os.getenv('BASE_URL')}/gym-owners?adminId={data['id']}"
    data['subject'] = 'Gym Insight - Updated Gym Details Verification'
    response = sendEmailNotification(data, emailTemplateConfigs['UPDATED_DOCUMENT_APPROVAL_REJECT'])
    if response['status']:
        print(f"updated gym details successfully send to super admin")

@shared_task
def documentApprovalNotification(data):
    data['link'] = f"{os.getenv('BASE_URL')}/gym-members"
    data['subject'] = 'Gym Insight - Gym Details Approved'
    response = sendEmailNotification(data, emailTemplateConfigs['DOCUMENT_APPROVAL'])
    if response['status']:
        print(f"Approval Notification successfully send to admin")

@shared_task
def documentRejectedNotification(data):
    data["link"] = f"{os.getenv('BASE_URL')}/dashboard?adminId={data['id']}"
    data["subject"] = 'Gym Insight - Gym Details Rejected'
    response = sendEmailNotification(data, emailTemplateConfigs['DOCUMENT_REJECTED'])
    if response['status']:
        print(f"Rejected Notification successfully send to admin")

@shared_task
def feesRenewalNotification(data): 
    data["subject"] = 'Gym Insight - Gym Fees Renewal'
    response = sendEmailNotification(data, emailTemplateConfigs['FEES_RENEWAL'])
    if response['status']:
        print(f"Fees Renewal Notification successfully send to {data['email']}")       

    
 


    
