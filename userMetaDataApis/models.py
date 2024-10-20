from django.db import models
from userApis.models import User
import uuid
from adminMetaDataApis.models import AdminMetaData
class UserMetaData(models.Model):
    user_meta_data_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_data')
    admin_id = models.ForeignKey(AdminMetaData, on_delete=models.CASCADE, to_field='admin_id', db_column='admin_id', related_name='users_metadata')
    trainer_assigned_name = models.CharField(max_length=50, null=True, blank=True)
    shift = models.CharField(max_length=10)
    last_fees_submission_date = models.DateField()
    renewal_date = models.DateField()
    current_plan_months = models.IntegerField()
    fees = models.IntegerField()
    payment_method = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Metadata for {self.user_id}'
    