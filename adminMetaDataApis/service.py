from .models import AdminMetaData, AdminDocumentData
from fileUpload.deleteFile import deleteFile
from .serializers import AdminDocumentDataSerializer, AdminMetaDataSerializer
from rest_framework import status

def create(payload, upload):
    try:
        adminMetaData, documentData = dtoToModel(payload, upload)

        # Validate and save AdminMetaData
        createMetaDataSerializer = AdminMetaDataSerializer(data=adminMetaData)
        if createMetaDataSerializer.is_valid():
            createMetaDataSerializer.save()
        else:
            for file in upload:
                deleteFile(upload[file]["fileId"])
            return {"error": createMetaDataSerializer.errors}, status.HTTP_400_BAD_REQUEST

        # Update AdminDocumentData
        document = AdminDocumentData.objects.get(admin_id=payload.get('adminId'))
        updateDocumentSerializer = AdminDocumentDataSerializer(document, data=documentData, partial=True)
        if updateDocumentSerializer.is_valid():
            updateDocumentSerializer.save()
            return {"message": "Admin data created successfully"}, status.HTTP_201_CREATED
        else:
            for file in upload:
                deleteFile(upload[file]["fileId"])
            return {"error": updateDocumentSerializer.errors}, status.HTTP_400_BAD_REQUEST

    except AdminDocumentData.DoesNotExist:
        for file in upload:
            deleteFile(upload[file]["fileId"])
        return {"error": "Document not found"}, status.HTTP_404_NOT_FOUND
    except Exception as e:
        for file in upload:
            deleteFile(upload[file]["fileId"])
        return {"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR

def dtoToModel(payload, upload):
    metaData = {
        "admin_id": payload.get('adminId'),
        "gym_name": payload.get('gymName'),
        "gym_address": payload.get('gymAddress'),
        "gym_city": payload.get('gymCity'),
        "gym_phone_no": payload.get('gymPhoneNo'),
        "gym_gst_no": payload.get('gymGstNo'),
    }
    documentData = {
        "gym_certificate_storage_path": upload['gym_certificate']['url'],
        "gym_logo_storage_path": upload['gym_logo']['url'],
        "gym_license_storage_path": upload['gym_license']['url']
    }
    return metaData, documentData
