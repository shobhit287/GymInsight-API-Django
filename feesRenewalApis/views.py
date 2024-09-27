from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
from authApis.jwt import validateJwt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from . import service


class FeesRenewal(APIView):

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Fees renewal emails Send Successfully",
            ),
            403: openapi.Response(
                description="Forbidden: You don't have access to perform this action."
            ),
            404: openapi.Response(
                description="admin not found"
            ),
            500: openapi.Response(
                description="Internal Server Error"
            )
        }
    ) 
    def post(self,request):
        validate = validateJwt(request.headers.get('Authorization'))
        if validate['status']:
            if validate['user']['role'] == "ADMIN":
                response, status = service.notifyAll(validate['user'])
                return JsonResponse(response, status= status)
            else:
                return JsonResponse({"error":"You don't have access to perform this action"}, status = status.HTTP_403_FORBIDDEN)
        else:
            return JsonResponse(validate, status= validate['code'])
        

class FeesRenewalById(APIView):

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Fees renewal email Send Successfully",
            ),
            403: openapi.Response(
                description="Forbidden: You don't have access to perform this action."
            ),
            404: openapi.Response(
                description="user not found"
            ),
            500: openapi.Response(
                description="Internal Server Error"
            )
        }
    ) 
    def post(self,request, id):
        validate = validateJwt(request.headers.get('Authorization'))
        if validate['status']:
            if validate['user']['role'] == "ADMIN":
                response, status = service.notifyById(validate['user'], id)
                return JsonResponse(response, status= status)
            else:
                return JsonResponse({"error":"You don't have access to perform this action"}, status = status.HTTP_403_FORBIDDEN)
        else:
            return JsonResponse(validate, status= validate['code'])
        

