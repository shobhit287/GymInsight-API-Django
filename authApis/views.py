from rest_framework.views import APIView
from django.http import JsonResponse,  HttpResponseRedirect
from rest_framework import status
from . import jwt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from . import service
from gymInsight.settings import BASE_URL

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
            response, code = service.login(payload)
            return JsonResponse(response, status = code)

        else:
            return JsonResponse({'error':'Data is missing'}, status=status.HTTP_400_BAD_REQUEST)
        
class AuthGoogleLogin(APIView):
      @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'token': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['token']
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
        if payload.get('token'):
            response, code = service.googleAuthLogin(payload)
            return JsonResponse(response, status = code)
        else:
            return JsonResponse({'error':'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)
        
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
            response, code = service.forgetPassword(payload)
            return JsonResponse(response, status = code)
        else:
            return JsonResponse({'error':'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
      

class AuthVerifyToken(APIView):  
    def get(self,request, token):
        validateToken = jwt.validateJwt(token)
        if validateToken['status']:
            return  HttpResponseRedirect(f"{BASE_URL}/reset-password?token={token}")
        else:
            return JsonResponse(validateToken, status= validateToken['code'])         

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
            response, code = service.resetPassword(payload,token)
            return JsonResponse(response, status = code)
        else:
            return JsonResponse({'error':'password is required'}, status=status.HTTP_400_BAD_REQUEST)            