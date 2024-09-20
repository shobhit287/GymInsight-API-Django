from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from . import service

class Auth(APIView):
      @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD)
            },
            required=['password','email']
        ),
        responses={
            200: openapi.Response(
                description="Login successfully"
            ),
            400: openapi.Response(
                description="Bad request"
            ),
            401: openapi.Response(
                description="Unauthorized"
            )
        }
    )
      def post(self,request):
        payload = request.data
        if payload:
            response = service.login(payload)
            return response

        else:
            return JsonResponse({'error':'Data is missing'}, status=status.HTTP_400_BAD_REQUEST)
        
class AuthForgetPassword(APIView):
      @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
            },
            required=['email']
        ),
        responses={
            200: openapi.Response(
                description="Password reset link sent"
            ),
            400: openapi.Response(
                description="Invalid Email"
            ),
        }
    )
      def post(self,request):
        payload = request.data
        if payload:
            response = service.forgetPassword(payload)
            return response
        else:
            return JsonResponse({'error':'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
      

class AuthVerifyToken(APIView):  
    def get(self,request, token):
            response = service.verifyResetToken(token)
            return response          

class AuthResetPassword(APIView):
      @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
            },
            required=['password']
        ),
        responses={
            200: openapi.Response(
                description="Password reset Successfully"
            ),
            400: openapi.Response(
                description="Bad Request"
            ),
        }
    )
      def post(self,request,token):
        payload = request.data
        if payload:
            response = service.resetPassword(payload,token)
            return response
        else:
            return JsonResponse({'error':'password is required'}, status=status.HTTP_400_BAD_REQUEST)            