from django.db import models
from userApis.models import User
from . statusEnum import status

class AdminMetaData(models.Model):
     admin_id = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, to_field='user_id', db_column='admin_id', unique= True)
     gym_name = models.TextField()
     gym_address = models.TextField()
     gym_city = models.CharField(max_length=50)
     gym_phone_no = models.CharField(max_length=10)
     gym_gst_no = models.CharField(max_length=15, unique=True)
     default_users_password = models.CharField(max_length=128)
     created_at = models.DateTimeField(auto_now_add= True)
     updated_at = models.DateTimeField(auto_now= True)
     def __str__(self):
          return self.gym_name

class AdminDocumentData(models.Model):
     admin_id = models.OneToOneField(User,primary_key=True, on_delete=models.CASCADE, to_field='user_id', db_column='admin_id', unique= True)
     gym_certificate_storage_path = models.TextField(null= True)
     gym_logo_storage_path = models.TextField(null = True)
     gym_license_storage_path = models.TextField(null = True)
     status = models.CharField(max_length=10,choices= status, null= True, blank=True)
     rejected_reason = models.TextField(null=True, blank=True)
     rejected_summary = models.TextField(null =True, blank= True)
     created_at = models.DateTimeField(auto_now_add= True)
     updated_at = models.DateTimeField(auto_now=True)
     def __str__(self):
          return self.admin_id.first_name
     
