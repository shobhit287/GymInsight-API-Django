from django.http import JsonResponse
from rest_framework.views import APIView
from . import service
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from authApis.jwt import validateJwt
from drf_yasg import openapi
from django.http import JsonResponse

class User(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'firstName': openapi.Schema(type=openapi.TYPE_STRING),
                'lastName': openapi.Schema(type=openapi.TYPE_STRING),
                'role': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD)
            },
            required=['firstName', 'lastName', 'email', 'role', 'password']
        ),
        responses={
            201: openapi.Response(
                description="User Created Successfully"
            ),
            400: openapi.Response(
                description="Bad request"
            ),
            500: openapi.Response(
                description="Internal Server Error"
            )
        }
    )
    def post(self, request):
        payload = request.data
        response,statusCode = service.create(payload)
        return JsonResponse(response, status=statusCode)

      

class UserById(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="User Details"
            ),
            404: openapi.Response(
                description="Not Found"
            ),
            500: openapi.Response(
                description="Internal Server Error"
            )
        }
    )
    def get(self, request, id):
        validateToken = validateJwt(request.headers.get('Authorization'))
        if(validateToken['status']):
                response, code = service.getById(id)
                return JsonResponse(response, status= code)
        else:
            return JsonResponse(validateToken, status = validateToken['code'])  
  
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'firstName': openapi.Schema(type=openapi.TYPE_STRING),
                'lastName': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
            },
        ),
        responses={
            201: openapi.Response(
                description="User Updated Successfully"
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
    def put(self, request, id):
        validateToken = validateJwt(request.headers.get('Authorization'))
        if(validateToken['status']):
                payload = request.data
                response, code = service.update(id, payload)
                return JsonResponse(response, status= code)
            
        else:
            return JsonResponse(validateToken, validateToken['code'])  
          
    # @swagger_auto_schema(
    #     responses={
    #         200: openapi.Response(
    #             description="User Deleted Successfully"
    #         ),
    #         404: openapi.Response(
    #             description="Not Found"
    #         ),
    #         403: openapi.Response(
    #             description="Forbidden: You don't have access to perform this action."
    #         ),
    #         500: openapi.Response(
    #             description="Internal Server Error"
    #         )
    #     }
    # )
    # def delete(self, request, id):
    #     validateToken = validateJwt(request.headers.get('Authorization'))
    #     if(validateToken['status']):
    #         if validateToken['user']['role'] == "ADMIN" :
    #             response, code = serviceUser.delete(id)
    #             return JsonResponse(response, status= code)
    #         else:
    #             return JsonResponse({"error": "You don't have access to perform this action."}, status=status.HTTP_403_FORBIDDEN)
    #     else:
    #         return JsonResponse(validateToken, validateToken['code'])    

class UserChangePassword(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'newPassword': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
                'oldPassword': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
            },
            required=['oldPassword', 'newPassword']
        ),
        responses={
            200: openapi.Response(
                description="Password Changed Successfully"
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
    def post(self, request, id):
        validateToken = validateJwt(request.headers.get('Authorization'))
        if(validateToken['status']):
                payload = request.data
                response, code = service.changePassword(id, payload)
                return JsonResponse(response, status= code)
        else:
            return JsonResponse(validateToken, validateToken['code'])     
