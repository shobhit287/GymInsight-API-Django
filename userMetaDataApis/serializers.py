from rest_framework import serializers
from . models import UserMetaData
from userApis.serializers import UserSerializer

class UserMetaDataSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user_id', read_only=True)    
    class Meta:
        model = UserMetaData
        fields = ['user_meta_data_id', 'user_id', 'admin_id', 'trainer_assigned_name', 'shift', 'last_fees_submission_date', 'renewal_date', 'current_plan_months', 'payment_method', 'fees', 'user_details', 'created_at', 'updated_at']
        extra_kwargs = {
            'user_meta_data_id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}, 
        }
        def create(self, validated_data):
            userMetaData = UserMetaData(
                admin_id = validated_data.get('admin_id'),
                user_id = validated_data.get('user_id'),
                trainer_assigned_name = validated_data.get('trainer_assigned_name'),
                shift = validated_data.get('shift'),
                last_fees_submission_date = validated_data.get('last_fees_submission_date'),
                renewal_date = validated_data.get('renewal_date'),
                current_plan_months = validated_data.get('current_plan_months'),
                fees = validated_data.get('fees'),
                payment_method = validated_data.get('payment_method')
            )
            userMetaData.save()
            return userMetaData
        
        def update(self, instance, validated_data):
            instance.trainer_assigned_name = validated_data.get('trainer_assigned_name', instance.trainer_assigned_name)
            instance.shift = validated_data.get('shift', instance.shift)
            instance.last_fees_submission_date = validated_data.get('joining_date', instance.last_fees_submission_date)
            instance.renewal_date = validated_data.get('renewal_date', instance.renewal_date)
            instance.current_plan_months = validated_data.get('current_plan_months', instance.current_plan_months)
            instance.payment_method = validated_data.get('payment_method', instance.payment_method)
            instance.fees = validated_data.get('fees', instance.fees)
            instance.save()
            return instance

