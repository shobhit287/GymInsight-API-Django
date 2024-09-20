import os
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from userApis.models import User

class Command(BaseCommand):
    help = 'Create superadmin if it does not exist'

    def handle(self, *args, **options):
        if not User.objects.filter(role="SUPER_ADMIN").exists():
            user = User(
                first_name=os.environ.get('SUPER_ADMIN_FIRST_NAME'),
                last_name=os.environ.get('SUPER_ADMIN_LAST_NAME'),
                email=os.environ.get('SUPER_ADMIN_EMAIL'),
                password=make_password(os.environ.get('SUPER_ADMIN_PASSWORD')),
                role="SUPER_ADMIN"
            )
            user.save()
            self.stdout.write(self.style.SUCCESS('Super admin created.'))
