from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
from authApis.jwt import validateJwt
from . helper import findAdminDocument
from drf_yasg import openapi
from . fileUploadService import uploadMetaFiles, updateMetaFiles
from . import service
from django.http import JsonResponse

class AdminMetaData(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter('adminId', openapi.IN_FORM, description="Admin ID ", type=openapi.TYPE_STRING, required=True),
        openapi.Parameter('gymName', openapi.IN_FORM, description="Gym Name", type=openapi.TYPE_STRING, required=True),
        openapi.Parameter('gymAddress', openapi.IN_FORM, description="Gym Address", type=openapi.TYPE_STRING, required=True),
        openapi.Parameter('gymCity', openapi.IN_FORM, description="Gym City", type=openapi.TYPE_STRING, required=True),
        openapi.Parameter('gymPhoneNo', openapi.IN_FORM, description="Gym Phone Number", type=openapi.TYPE_STRING, required=True),
        openapi.Parameter('gymGstNo', openapi.IN_FORM, description="Gym GST Number", type=openapi.TYPE_STRING, required=True),
        openapi.Parameter('gymLogo', openapi.IN_FORM, description="Gym Logo (File)", type=openapi.TYPE_FILE, required=True),
        openapi.Parameter('gymCertificate', openapi.IN_FORM, description="Gym Certification (File)", type=openapi.TYPE_FILE, required=True),
        openapi.Parameter('gymLicense', openapi.IN_FORM, description="Gym License (File)", type=openapi.TYPE_FILE, required=True),
    ],
    responses={
        201: openapi.Response(description="Admin Meta Data Created Successfully"),
        400: openapi.Response(description="Bad Request"),
        403: openapi.Response(description="You don't have access to perform this action."),
        404: openapi.Response(description="Admin Not Found"),
        500: openapi.Response(description="Internal Server Error"),
    },
    consumes=['multipart/form-data']
    )
    def post(self,request):
        validateToken = validateJwt(request.headers.get('Authorization'))
        if validateToken['status']:
            if(validateToken['user']['role']=="ADMIN"):
                payload = request.data
                if not payload:
                    return JsonResponse({"error":"Data is missing"}, status = status.HTTP_400_BAD_REQUEST)
                upload,code = uploadMetaFiles({
                    'gym_logo': payload.get('gymLogo'),
                    'gym_certificate': payload.get('gymCertificate'),
                    'gym_license': payload.get('gymLicense')
                })
                if code == 201:
                    response,statusCode = service.create(payload, upload)
                    return JsonResponse(response, status= statusCode)
                else:
                    return JsonResponse(upload, status=code)
            else:
                return JsonResponse({"error": "You don't have access to perform this action."}, status=status.HTTP_403_FORBIDDEN)   
        else: 
            return JsonResponse(validateToken,status= validateToken['code'])    

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="List of all admin Meta Data",
            ),
            404: openapi.Response(
                description="Document Not Found"
            ),
            403: openapi.Response(
                description="Forbidden: You don't have access to perform this action."
            ),
            500: openapi.Response(
                description="Internal Server Error"
            )
        }
    )  
    def get(self,request):
        validateToken = validateJwt(request.headers.get('Authorization'))
        if validateToken['status']:
            if(validateToken['user']['role']=="SUPER_ADMIN"):
                response, statusCode = service.getAll()
                return JsonResponse(response, status= statusCode)
            else:
                return JsonResponse({"error": "You don't have access to perform this action."}, status=status.HTTP_403_FORBIDDEN)   
        else: 
            return JsonResponse(validateToken,status= validateToken['code'])    
      

class AdminMetaDataById(APIView):
    parser_classes = (MultiPartParser, FormParser)
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Detail of admin meta data",
            ),
            404: openapi.Response(
                description="Admin not found"
            ),
            403: openapi.Response(
                description="Forbidden: You don't have access to perform this action."
            ),
            500: openapi.Response(
                description="Internal Server Error"
            )
        }
    )
    def get(self,request, id):
        validateToken = validateJwt(request.headers.get('Authorization'))
        if validateToken['status']:
            if(validateToken['user']['role'] != "USER"):
                response, statusCode = service.getById(id)
                return JsonResponse(response, status= statusCode)
            else:
                return JsonResponse({"error": "You don't have access to perform this action."}, status=status.HTTP_403_FORBIDDEN)   
        else: 
            return JsonResponse(validateToken,status= validateToken['code'])

    @swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter('gymName', openapi.IN_FORM, description="Gym Name", type=openapi.TYPE_STRING, required=False),
        openapi.Parameter('gymAddress', openapi.IN_FORM, description="Gym Address", type=openapi.TYPE_STRING, required=False),
        openapi.Parameter('gymCity', openapi.IN_FORM, description="Gym City", type=openapi.TYPE_STRING, required=False),
        openapi.Parameter('gymPhoneNo', openapi.IN_FORM, description="Gym Phone Number", type=openapi.TYPE_STRING, required=False),
        openapi.Parameter('gymGstNo', openapi.IN_FORM, description="Gym GST Number", type=openapi.TYPE_STRING, required=False),
        openapi.Parameter('gymLogo', openapi.IN_FORM, description="Gym Logo (File)", type=openapi.TYPE_FILE, required=False),
        openapi.Parameter('gymCertificate', openapi.IN_FORM, description="Gym Certification (File)", type=openapi.TYPE_FILE, required=False),
        openapi.Parameter('gymLicense', openapi.IN_FORM, description="Gym License (File)", type=openapi.TYPE_FILE, required=False),
    ],
    responses={
        201: openapi.Response(description="Admin Meta Data Updated Successfully"),
        400: openapi.Response(description="Bad Request"),
        403: openapi.Response(description="You don't have access to perform this action."),
        404: openapi.Response(description="Admin Not Found"),
        500: openapi.Response(description="Internal Server Error"),
    },
    consumes=['multipart/form-data']
    )    
    def put(self,request, id):
        validateToken = validateJwt(request.headers.get('Authorization'))
        if validateToken['status']:
            if(validateToken['user']['role']=="ADMIN"):
                payload = request.data
                if not payload:
                    return JsonResponse({"error":"Data is missing"}, status = status.HTTP_400_BAD_REQUEST)

                adminDocument, isFound = findAdminDocument(id)
                if not isFound:
                    return JsonResponse({"error":"admin doc not found"}, status = status.HTTP_404_NOT_FOUND)
                
                elif adminDocument['status'] == "PENDING":
                    return JsonResponse({"error":"You cannot update your details as the document status is in 'Pending' state"}, status = status.HTTP_400_BAD_REQUEST)

                upload,code = updateMetaFiles({
                    'gym_logo': payload.get('gymLogo'),
                    'gym_certificate': payload.get('gymCertificate'),
                    'gym_license': payload.get('gymLicense')
                })
                if code == 201 or code == 200:
                    response,statusCode = service.update(id, payload, upload)
                    return JsonResponse(response, status= statusCode)
                else:
                    return JsonResponse(upload, status=code)
            else:
                return JsonResponse({"error": "You don't have access to perform this action."}, status=status.HTTP_403_FORBIDDEN)   
        else: 
            return JsonResponse(validateToken,status= validateToken['code'])
    
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Admin and gym members deleted Successfully",
            ),
            404: openapi.Response(
                description="Admin Not Found"
            ),
            403: openapi.Response(
                description="Forbidden: You don't have access to perform this action."
            ),
            500: openapi.Response(
                description="Internal Server Error"
            )
        }
    )
    def delete(self, request, id):
        validateToken = validateJwt(request.headers.get('Authorization'))
        if validateToken['status']:
            if(validateToken['user']['role'] != "USER"):
                response, statusCode = service.delete(id)
                return JsonResponse(response, status= statusCode)
            else:
                return JsonResponse({"error": "You don't have access to perform this action."}, status=status.HTTP_403_FORBIDDEN)   
        else: 
            return JsonResponse(validateToken,status= validateToken['code']) 

        
class AdminMetaDataApprove(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Status changes to approved",
            ),
            404: openapi.Response(
                description="Document Not Found"
            ),
            403: openapi.Response(
                description="Forbidden: You don't have access to perform this action."
            ),
            500: openapi.Response(
                description="Internal Server Error"
            )
        }
    )  
    def patch(self,request, id):
        validateToken = validateJwt(request.headers.get('Authorization'))
        if validateToken['status']:
            if(validateToken['user']['role'] == "SUPER_ADMIN"):
                response, statusCode = service.approve(id)
                return JsonResponse(response, status= statusCode)
            else:
                return JsonResponse({"error": "You don't have access to perform this action."}, status=status.HTTP_403_FORBIDDEN)   
        else: 
            return JsonResponse(validateToken,status= validateToken['code']) 
        
class AdminMetaDataReject(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'rejectedReason': openapi.Schema(type=openapi.TYPE_STRING),
                'rejectedSummary': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['rejectedReason', 'rejectedSummary']
        ),
        responses={
            200: openapi.Response(
                description="Status changes to reject",
            ),
            404: openapi.Response(
                description="Document Not Found"
            ),
            403: openapi.Response(
                description="Forbidden: You don't have access to perform this action."
            ),
            500: openapi.Response(
                description="Internal Server Error"
            )
        }
    )  
    def patch(self,request, id):
        validateToken = validateJwt(request.headers.get('Authorization'))
        if validateToken['status']:
            if(validateToken['user']['role'] == "SUPER_ADMIN"):
                response, statusCode = service.reject(request.data, id)
                return JsonResponse(response, status= statusCode)
            else:
                return JsonResponse({"error": "You don't have access to perform this action."}, status=status.HTTP_403_FORBIDDEN)   
        else: 
            return JsonResponse(validateToken,status= validateToken['code']) 

