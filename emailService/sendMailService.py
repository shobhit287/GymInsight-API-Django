import os
from dotenv import load_dotenv
from .emailTemplateConfig import emailTemplateConfigs
from .sendEmail import sendEmailNotification
load_dotenv()
def passwordResetSendNotification(data):
    dynamicData= {
                  "userName" : f"{data['first_name']} {data['last_name']}",
                  "email":data['email'],
                  "link" : f"{os.getenv('BASE_URL')}?token={data['token']}",
                  "subject": 'Password Reset Request'
                }
    response = sendEmailNotification(dynamicData, emailTemplateConfigs['PASSWORD_RESET_TEMPLATE'])
    if response['status']:
        print(f"password reset email send successfully to {dynamicData['email']}")
        return {'message': 'Reset link sent to your mail', "status": True}
    else: 
        return response
    
def sendAdminUserCreateNotification(data):
    data["link"] = f"{os.getenv('BASE_URL')}/login"
    data["subject"] = 'Gym Insight Admin Credentials'
    response = sendEmailNotification(data, emailTemplateConfigs['ADMIN_CREDENTIALS_TEMPLATE'])
    if response['status']:
        print(f"admin credentials  send successfully to {data['email']}")

def sendUserCreateNotification(data):
    data["link"] = f"{os.getenv('BASE_URL')}/login"
    data["subject"] = 'Gym Insight User Credentials'
    response = sendEmailNotification(data, emailTemplateConfigs['USER_CREDENTIALS_TEMPLATE'])
    if response['status']:
        print(f"user credentials  send successfully to {data['email']}")


def documentApprovalRejectNotification(data):
    data['link'] = f"{os.getenv('BASE_URL')}/gym-details/?adminId={data['id']}"
    data['subject'] = 'Gym Insight - Gym Details Verification'
    response = sendEmailNotification(data, emailTemplateConfigs['DOCUMENT_APPROVAL_REJECT'])
    if response['status']:
        print(f"Gym details send successfully to super admin")

def updatedDocumentApprovalRejectNotification(data):
    data['link'] = f"{os.getenv('BASE_URL')}/gym-details/?adminId={data['id']}"
    data['subject'] = 'Gym Insight - Updated Gym Details Verification'
    response = sendEmailNotification(data, emailTemplateConfigs['UPDATED_DOCUMENT_APPROVAL_REJECT'])
    if response['status']:
        print(f"updated gym details successfully send to super admin")

def documentApprovalNotification(data):
    data['link'] = f"{os.getenv('BASE_URL')}/dashboard"
    data['subject'] = 'Gym Insight - Gym Details Approved'
    response = sendEmailNotification(data, emailTemplateConfigs['DOCUMENT_APPROVAL'])
    if response['status']:
        print(f"updated gym details successfully send to super admin")

def documentRejectedNotification(data):
    data["link"] = f"{os.getenv('BASE_URL')}/gym-details/edit",
    data["subject"] = 'Gym Insight - Gym Details Approved',
    response = sendEmailNotification(data, emailTemplateConfigs['DOCUMENT_REJECTED'])
    if response['status']:
        print(f"Rejected Notification successfully send to super admin")

    
 


    
