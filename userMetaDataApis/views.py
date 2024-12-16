from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from . import service
from django.http import JsonResponse
from authApis.jwt import validateJwt
from rest_framework import status

class UserMetaData(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'userId': openapi.Schema(type=openapi.TYPE_STRING),
                'trainerName': openapi.Schema(type=openapi.TYPE_STRING),
                'lastFeesDate': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                'renewalDate': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                'paymentMethod': openapi.Schema(type=openapi.TYPE_STRING),
                'currentPlanDuration': openapi.Schema(type=openapi.TYPE_STRING),
                'fees': openapi.Schema(type=openapi.TYPE_STRING),
                'shift': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['userId', 'trainerName', 'lastFeesDate', 'renewalDate','paymentMethod', 'currentPlanDuration', 'shift']
        ),
        responses={
            201: openapi.Response(
                description="User Meta Data Created Successfully"
            ),
            400: openapi.Response(
                description="Bad request"
            ),
            403: openapi.Response(
                description="Forbidden: You don't have access to perform this action."
            ),
            500: openapi.Response(
                description="Internal Server Error"
            )
        }
    )
    def post(self, request):
        validate= validateJwt(request.headers.get('Authorization'))
        if validate['status']:
            if validate['user']['role'] == "ADMIN":
                response, statusCode = service.create(request.data, validate['user'])
                return JsonResponse(response, status = statusCode)
            else:
                return JsonResponse({"error":"You don't have access to perform this action"}, status = status.HTTP_403_FORBIDDEN)
        else:
            return JsonResponse(validate, status= validate['code'])  

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="List of all User Meta Data",
            ),
            403: openapi.Response(
                description="Forbidden: You don't have access to perform this action."
            ),
            500: openapi.Response(
                description="Internal Server Error"
            )
        }
    )      
    def get(self, request):
        validate= validateJwt(request.headers.get('Authorization'))
        if validate['status']:
            if validate['user']['role'] == "ADMIN":
                response, statusCode = service.getAll(validate['user'])
                return JsonResponse(response, status = statusCode)
            else:
                return JsonResponse({"error":"You don't have access to perform this action"}, status = status.HTTP_403_FORBIDDEN)
        else:
            return JsonResponse(validate, status= validate['code'])    
            


class UserMetaDataById(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Detial of User Meta Data",
            ),
            403: openapi.Response(
                description="Forbidden: You don't have access to perform this action."
            ),
            404: openapi.Response(
                description="User not found"
            ),
            500: openapi.Response(
                description="Internal Server Error"
            )
        }
    ) 
    def get(self, request, id):
        validate= validateJwt(request.headers.get('Authorization'))
        if validate['status']:
            if validate['user']['role'] != "SUPER_ADMIN":
                response, statusCode = service.getById(id)
                return JsonResponse(response, status = statusCode)
            else:
                return JsonResponse({"error":"You don't have access to perform this action"}, status = status.HTTP_403_FORBIDDEN)
        else:
            return JsonResponse(validate, status= validate['code']) 
        
    

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'trainerName': openapi.Schema(type=openapi.TYPE_STRING),
                'lastFeesDate': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                'renewalDate': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                'paymentMethod': openapi.Schema(type=openapi.TYPE_STRING),
                'currentPlanDuration': openapi.Schema(type=openapi.TYPE_STRING),
                'fees': openapi.Schema(type=openapi.TYPE_STRING),
                'shift': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            201: openapi.Response(
                description="User Meta Data Created Successfully"
            ),
            400: openapi.Response(
                description="Bad request"
            ),
            403: openapi.Response(
                description="Forbidden: You don't have access to perform this action."
            ),
            404: openapi.Response(
                description="user meta data not found"
            ),
            500: openapi.Response(
                description="Internal Server Error"
            )
        }
    )
    def put(self, request, id):
        validate= validateJwt(request.headers.get('Authorization'))
        if validate['status']:
            if validate['user']['role'] == "ADMIN":
                response, statusCode = service.update(validate['user'], id, request.data)
                return JsonResponse(response, status = statusCode)
            else:
                return JsonResponse({"error":"You don't have access to perform this action"}, status = status.HTTP_403_FORBIDDEN)
        else:
            return JsonResponse(validate, status= validate['code']) 
        
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="User Deleted Successfully",
            ),
            403: openapi.Response(
                description="Forbidden: You don't have access to perform this action."
            ),
            404: openapi.Response(
                description="User not found"
            ),
            500: openapi.Response(
                description="Internal Server Error"
            )
        }
    ) 
    def delete(self, request, id):
        validate= validateJwt(request.headers.get('Authorization'))
        if validate['status']:
            if validate['user']['role'] == "ADMIN":
                response, statusCode = service.delete(validate['user'], id)
                return JsonResponse(response, status = statusCode)
            else:
                return JsonResponse({"error":"You don't have access to perform this action"}, status = status.HTTP_403_FORBIDDEN)
        else:
            return JsonResponse(validate, status= validate['code'])     

class RequestPlan(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'currentWeight': openapi.Schema(type=openapi.TYPE_STRING),
                'goalWeight': openapi.Schema(type=openapi.TYPE_STRING),
                'height': openapi.Schema(type=openapi.TYPE_STRING),
                'isDiet': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                'isExerciseSchedule': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            },
            required=['currentWeight','goalWeight', 'height', 'isDiet', 'isExerciseSchedule']
        ),
        responses={
            200: openapi.Response(description="Admin Notified Successfully"),
            400: openapi.Response(description="Bad request"),
            403: openapi.Response(description="Forbidden: You don't have access to perform this action."),
            404: openapi.Response(description="User meta data not found"),
            500: openapi.Response(description="Internal Server Error"),
        }
    )
    def post(self, request):
        # Your logic to handle the POST request
        validate = validateJwt(request.headers.get('Authorization'))
        if validate['status']:
            if validate['user']['role'] == "USER":
                response, statusCode = service.requestPlan(validate['user'], request.data)
                return JsonResponse(response, status=statusCode)
            else:
                return JsonResponse({"error":"You don't have access to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return JsonResponse(validate, status=validate['code'])
