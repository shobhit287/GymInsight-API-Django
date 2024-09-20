from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
def sendEmailNotification(dynamicData, template):
    msgHtml = render_to_string(template, dynamicData)
    try:
        msg = EmailMultiAlternatives(
            subject=dynamicData['subject'],
            to=[dynamicData['email']],
        )
        msg.attach_alternative(msgHtml, "text/html")
        msg.send()
        return {'status':True}
    except Exception as e:
        print("Error:", e)
        return {'status':False, 'error': e}