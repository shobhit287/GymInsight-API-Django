import os
from dotenv import load_dotenv
from .emailTemplateConfig import emailTemplateConfigs
from .sendEmail import sendEmailNotification
load_dotenv()
def passwordResetSendNotification(data):
    dynamicData= {"userName" : f"{data['first_name']} {data['last_name']}",
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
    dynamicData= {
                "userName" : f"{data['first_name']} {data['last_name']}",
                "email":data['email'],
                "password":data['password'] ,
                "link" : f"{os.getenv('BASE_URL')}/login",
                "subject": 'Gym Insight Admin Credentials',
            }
    response = sendEmailNotification(dynamicData, emailTemplateConfigs['ADMIN_CREDENTIALS_TEMPLATE'])
    if response['status']:
        print(f"admin credentials  send successfully to {dynamicData['email']}")

def sendUserCreateNotification(data):
    dynamicData= {
                "userName" : f"{data['first_name']} {data['last_name']}",
                "email":data['email'],
                "password":data['password'] ,
                "link" : f"{os.getenv('BASE_URL')}/login",
                "subject": 'Gym Insight User Credentials',
            }
    response = sendEmailNotification(dynamicData, emailTemplateConfigs['USER_CREDENTIALS_TEMPLATE'])
    if response['status']:
        print(f"user credentials  send successfully to {dynamicData['email']}")

    
 


    
