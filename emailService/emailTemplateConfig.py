import os
from django.conf import settings

emailTemplateConfigs = {
    "PASSWORD_RESET_TEMPLATE": os.path.join(settings.BASE_DIR, "emailService", "templates","password-reset.html"),
    "ADMIN_CREDENTIALS_TEMPLATE": os.path.join(settings.BASE_DIR, "emailService", "templates","admin-credentials.html"),
    "USER_CREDENTIALS_TEMPLATE": os.path.join(settings.BASE_DIR, "emailService", "templates","user-credentials.html")
}