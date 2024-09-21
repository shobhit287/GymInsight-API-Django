from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
from authApis.jwt import validateJwt
from drf_yasg import openapi
from . fileUploadService import uploadMetaFiles
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
      

