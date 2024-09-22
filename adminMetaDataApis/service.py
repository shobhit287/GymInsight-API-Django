from .models import AdminMetaData, AdminDocumentData
from fileUpload.deleteFile import deleteFile
from .serializers import AdminDocumentDataSerializer, AdminMetaDataSerializer
from rest_framework import status
from userApis.models import User
from userApis.helper import findOne, findOneByRole
from emailService.sendMailService import documentApprovalRejectNotification, updatedDocumentApprovalRejectNotification, documentApprovalNotification, documentRejectedNotification
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
            user = findOne(payload.get('adminId'))
            superAdmin= findOneByRole("SUPER_ADMIN")
            documentApprovalRejectNotification({
                "userName": f"{user['user']['first_name']} {user['user']['last_name']}",
                "email": superAdmin['user']['email'],
                "id": payload.get('adminId')
            })
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
        return {"error": "An unexpected error occur"}, status.HTTP_500_INTERNAL_SERVER_ERROR
    
def getAll():
    try:
        adminMeta = AdminMetaData.objects.all().order_by('-updated_at')
        adminMetaSerializer = AdminMetaDataSerializer(adminMeta, many = True)
        structuredResponse = []
        for adminMeta in adminMetaSerializer.data:
            adminDocument = AdminDocumentData.objects.get(admin_id= adminMeta.get('admin_id'))
            adminDocumentSerializer = AdminDocumentDataSerializer(adminDocument)
            structuredData = modelToDto(adminMeta, adminDocumentSerializer.data)
            structuredResponse.append(structuredData)
        return {"data": structuredResponse}, 200    
    except AdminDocumentData.DoesNotExist:
        return {"error": "Document not found"}, status.HTTP_404_NOT_FOUND
    except Exception as e:
        return {"error": "An unexpected error occur"}, status.HTTP_500_INTERNAL_SERVER_ERROR
    
def getById(id):
    try:
        adminMeta = AdminMetaData.objects.get(admin_id = id)
        adminMetaSerializer = AdminMetaDataSerializer(adminMeta)
        adminDocument = AdminDocumentData.objects.get(admin_id= id)
        adminDocumentSerializer = AdminDocumentDataSerializer(adminDocument)
        return {"data": modelToDto(adminMetaSerializer.data, adminDocumentSerializer.data)}, 200    
    except AdminMetaData.DoesNotExist:
        return {"error": "Admin not found"}, status.HTTP_404_NOT_FOUND
    except Exception as e:
        return {"error": "An unexpected error occur"}, status.HTTP_500_INTERNAL_SERVER_ERROR

def update(id, payload, upload):
    try:
        adminMetaData, documentData = updateDtoToModel(payload, upload)
        adminMeta = AdminMetaData.objects.get(admin_id = id)
        updateAdminMetaData = AdminMetaDataSerializer(adminMeta, data=adminMetaData, partial = True)
        if updateAdminMetaData.is_valid():
            updateAdminMetaData.save()
        else:
            for file in upload:
                deleteFile(upload[file]["fileId"])
            return {"error": updateAdminMetaData.errors}, status.HTTP_400_BAD_REQUEST
        

        # Update AdminDocumentData
        document = AdminDocumentData.objects.get(admin_id = id)
        updateDocumentSerializer = AdminDocumentDataSerializer(document, data=documentData, partial=True)
        if updateDocumentSerializer.is_valid():
            updateDocumentSerializer.save()
            user = findOne(payload.get('adminId'))
            superAdmin= findOneByRole("SUPER_ADMIN")
            updatedDocumentApprovalRejectNotification({
                "userName": f"{user['user']['first_name']} {user['user']['last_name']}",
                "email": superAdmin['user']['email'],
                "id": payload.get('adminId')
            })
            return {"message": "Admin data Updated successfully"}, status.HTTP_200_OK
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
        return {"error": "An unexpected error occur"}, status.HTTP_500_INTERNAL_SERVER_ERROR

def approve(id):
    try:
        document = AdminDocumentData.objects.get(admin_id = id)
        approveDocument = AdminDocumentDataSerializer(document, data={"status":"APPROVED"}, partial = True)
        if approveDocument.is_valid():
            approveDocument.save()
            user = findOne(id)
            documentApprovalNotification({
                "userName": f"{user['user']['first_name']} {user['user']['last_name']}",
                "email": user['user']['email'],
                "id": id
            })
            return {"message":"Status has been changed to 'Approved'"}, status.HTTP_200_OK
        else:
            return {"error": approveDocument.errors}, status.HTTP_400_BAD_REQUEST
    
    except AdminDocumentData.DoesNotExist:
        return {"error": "Document not found"}, status.HTTP_404_NOT_FOUND
    
    except Exception as e:
        return {"error": "An unexpected error occur"}, status.HTTP_500_INTERNAL_SERVER_ERROR
    
def reject(payload, id):
    try:
        if not payload.get('rejectedReason') and not payload.get('rejectedSummary'):
            return {"error":"Both 'Rejected Reason' and 'Rejected Summary' are required fields."}, status.HTTP_400_BAD_REQUEST
        document = AdminDocumentData.objects.get(admin_id = id)
        approveDocument = AdminDocumentDataSerializer(document, data={"status":"REJECTED", "rejected_reason": payload.get('rejectedReason'), "rejected_summary":payload.get('rejectedSummary')}, partial = True)
        if approveDocument.is_valid():
            approveDocument.save()
            user = findOne(id)
            documentRejectedNotification({
                "userName": f"{user['user']['first_name']} {user['user']['last_name']}",
                "email": user['user']['email'],
                "rejectedReason": payload.get('rejected_reason'),
                "rejectedSummary": payload.get('rejected_summary'),
                "id": id
            })
            return {"message":"Status has been changed to 'Rejected'"}, status.HTTP_200_OK
        else:
            return {"error": approveDocument.errors}, status.HTTP_400_BAD_REQUEST
    
    except AdminDocumentData.DoesNotExist:
        return {"error": "Document not found"}, status.HTTP_404_NOT_FOUND
    
    except Exception as e:
        return {"error": "An unexpected error occur"}, status.HTTP_500_INTERNAL_SERVER_ERROR

def delete(id):
    try:
        user = User.objects.get(user_id = id)
        user.delete()
        return {"message": "Admin and gym members deleted successfully"}, status.HTTP_200_OK
    except User.DoesNotExist:
        return {"error": "Admin not found"}, status.HTTP_404_NOT_FOUND
    except Exception as e:
        return {"error": "An unexpected error occurred"}, status.HTTP_500_INTERNAL_SERVER_ERROR


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


def modelToDto(adminMeta, adminDocument):
    return {
        "adminId" :  adminMeta.get('admin_id'),
        "gymName": adminMeta.get('gym_name'),
        "gymAddress": adminMeta.get('gym_address'),
        "gymCity": adminMeta.get('gym_city'),
        "gymPhoneNo": adminMeta.get('gym_phone_no'),
        "gymGstNo": adminMeta.get('gym_gst_no'),
        "documentData":{
            "documentId": adminDocument.get('document_id'),
            "gymCertificatePath": adminDocument.get('gym_certificate_storage_path'),
            "gymLicensePath": adminDocument.get('gym_license_storage_path'),
            "gymLogoPath": adminDocument.get('gym_logo_storage_path'),
            "rejectedReason": adminDocument.get('rejected_reason'),
            "rejectedSummary": adminDocument.get('rejected_summary'),
            "updatedAt": adminDocument.get('updated_at'),
            "createdAt": adminDocument.get('created_at'),
        },
        "status": adminDocument.get('status'),
        "updatedAt": adminMeta.get('updated_at'),
        "createdAt": adminMeta.get('created_at'),
    }

def updateDtoToModel(payload, upload):
    metaData = {}
    documentData = {}

    # Update metaData fields only if they are present in the payload
    if payload.get('gymName') is not None:
        metaData['gym_name'] = payload.get('gymName')
    if payload.get('gymAddress') is not None:
        metaData['gym_address'] = payload.get('gymAddress')
    if payload.get('gymCity') is not None:
        metaData['gym_city'] = payload.get('gymCity')
    if payload.get('gymPhoneNo') is not None:
        metaData['gym_phone_no'] = payload.get('gymPhoneNo')
    if payload.get('gymGstNo') is not None:
        metaData['gym_gst_no'] = payload.get('gymGstNo')

    # Update documentData fields only if they are present in the upload dictionary
    if upload.get('gym_certificate') is not None:
        documentData['gym_certificate_storage_path'] = upload['gym_certificate'].get('url')
    if upload.get('gym_logo') is not None:
        documentData['gym_logo_storage_path'] = upload['gym_logo'].get('url')
    if upload.get('gym_license') is not None:
        documentData['gym_license_storage_path'] = upload['gym_license'].get('url')

    documentData['status'] = "PENDING"    

    return metaData, documentData

