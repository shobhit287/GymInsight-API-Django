import os
from django.conf import settings

emailTemplateConfigs = {
    "PASSWORD_RESET_TEMPLATE": os.path.join(settings.BASE_DIR, "emailService", "templates","password-reset.html"),
    "ADMIN_CREDENTIALS_TEMPLATE": os.path.join(settings.BASE_DIR, "emailService", "templates","admin-credentials.html"),
    "USER_CREDENTIALS_TEMPLATE": os.path.join(settings.BASE_DIR, "emailService", "templates","user-credentials.html"),
    "DOCUMENT_APPROVAL_REJECT": os.path.join(settings.BASE_DIR, "emailService", "templates","document-approval-reject.html"),
    "UPDATED_DOCUMENT_APPROVAL_REJECT": os.path.join(settings.BASE_DIR, "emailService", "templates", "updated-document-approval-reject.html"),
    "DOCUMENT_APPROVAL": os.path.join(settings.BASE_DIR, "emailService", "templates", "document-approve.html"),
    "DOCUMENT_REJECTED": os.path.join(settings.BASE_DIR, "emailService", "templates", "document-reject.html"),
    "FEES_RENEWAL": os.path.join(settings.BASE_DIR, "emailService", "templates", "fees-renewal.html"),
}