from rest_framework import serializers
from . models import AdminDocumentData, AdminMetaData
from userApis.serializers import UserSerializer
from userMetaDataApis.serializers import UserMetaDataSerializer
class AdminMetaDataSerializer(serializers.ModelSerializer):
    admin_details = UserSerializer(source='admin_id', read_only=True)
    users_meta_data = UserMetaDataSerializer(source= 'users_metadata',many= True, read_only= True)
    class Meta:
        model = AdminMetaData
        fields = [
                  'admin_id',
                  'gym_name',
                  'gym_address',
                  'gym_city',
                  'gym_phone_no',
                  'default_users_password',
                  'admin_details',
                  'users_meta_data',
                  'gym_gst_no',
                  'created_at',
                  'updated_at'
                ]
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}, 
        }

        def create(self, validated_data):
            adminMetaData = AdminMetaData(
                admin_id = validated_data.get('admin_id'),
                gym_name = validated_data.get('gym_name'),
                gym_address = validated_data.get('gym_address'),
                gym_city = validated_data.get('gym_city'),
                gym_phone_no = validated_data.get('gym_phone_no'),
                gym_gst_no = validated_data.get('gym_gst_no'),
                default_users_password = validated_data.get('default_users_password')
            )
            adminMetaData.save()
            return adminMetaData
        
        def update(self,instance, validated_data):
            instance.gym_name = validated_data.get('gym_name', instance.gym_name)
            instance.gym_address = validated_data.get('gym_address', instance.gym_address)
            instance.gym_city = validated_data.get('gym_city', instance.gym_city)
            instance.gym_phone_no = validated_data.get('gym_phone_no', instance.gym_phone_no)
            instance.gym_gst_no = validated_data.get('gym_gst_no', instance.gym_gst_no)
            instance.default_users_password = validated_data.get('default_users_password', instance.default_users_password)
            instance.save()
            return instance
        
class AdminDocumentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminDocumentData
        fields = [
                  'admin_id',
                  'gym_certificate_storage_path',
                  'gym_logo_storage_path',
                  'gym_license_storage_path',
                  'status',
                  'rejected_reason',
                  'rejected_summary',
                  'created_at',
                  'updated_at'
                ]
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}, 
        }

        def create(self, validated_data):
            adminDocumentData = AdminDocumentData(
                admin_id = validated_data.get('admin_id'),
            )
            adminDocumentData.save()
            return adminDocumentData
        
        def update(self,instance, validated_data):
            instance.gym_certificate_storage_path = validated_data.get('gym_certificate_storage_path', instance.gym_certificate_storage_path)
            instance.gym_logo_storage_path = validated_data.get('gym_logo_storage_path', instance.gym_logo_storage_path)
            instance.gym_license_storage_path = validated_data.get('gym_license_storage_path', instance.gym_license_storage_path)
            instance.status = validated_data.get('status', instance.status)
            instance.rejected_reason = validated_data.get('rejected_reason', instance.rejected_reason)
            instance.rejected_summary = validated_data.get('rejected_summary', instance.rejected_summary)
            instance.save()
            return instance