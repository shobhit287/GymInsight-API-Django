from django.http import JsonResponse
from rest_framework.views import APIView
from . import serviceAdmin, serviceUser
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from authApis.jwt import validateJwt
from drf_yasg import openapi
from django.http import JsonResponse

class UserAdmin(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'firstName': openapi.Schema(type=openapi.TYPE_STRING),
                'lastName': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD)
            },
            required=['firstName', 'lastName', 'email', 'password']
        ),
        responses={
            201: openapi.Response(
                description="Admin Created Successfully"
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
        validateToken = validateJwt(request.headers.get('Authorization'))
        if validateToken['status']:
            if(validateToken['user']['role'] == "SUPER_ADMIN"):
                payload = request.data
                response,statusCode = serviceAdmin.createAdmin(payload)
                return JsonResponse(response, status=statusCode)
            else:
                return JsonResponse({"error": "You don't have access to perform this action."}, status=status.HTTP_403_FORBIDDEN)   
        else: 
            return JsonResponse(validateToken,status= validateToken['code']) 

    # @swagger_auto_schema(
    #     responses={
    #         200: openapi.Response(
    #             description="List of all admin users",
    #         ),
    #         400: openapi.Response(
    #             description="Bad request"
    #         ),
    #          403: openapi.Response(
    #             description="Forbidden: You don't have access to perform this action."
    #         ),
    #         500: openapi.Response(
    #             description="Internal Server Error"
    #         )
    #     }
    # )
    # def get(self, request):
    #     validateToken = validateJwt(request.headers.get('Authorization'))
    #     if validateToken['status']:
    #         if(validateToken['user']['role'] == "SUPER_ADMIN"):
    #             response,statusCode = serviceAdmin.getAllAdminUsers()
    #             return JsonResponse(response, status=statusCode)
    #         else:
    #             return JsonResponse({"error": "You don't have access to perform this action."}, status=status.HTTP_403_FORBIDDEN)   
    #     else: 
    #         return JsonResponse(validateToken,status= validateToken['code'])   

class UserAdminById(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Admin Details"
            ),
            404: openapi.Response(
                description="Not Found"
            ),
            403: openapi.Response(
                description="Forbidden: You don't have access to perform this action."
            ),
            500: openapi.Response(
                description="Internal Server Error"
            )
        }
    )
    def get(self, request, id):
        validateToken = validateJwt(request.headers.get('Authorization'))
        if(validateToken['status']):
            if validateToken['user']['role'] != "USER" :
                response, code = serviceAdmin.getById(id)
                return JsonResponse(response, status= code)
            else:
                return JsonResponse({"error": "You don't have access to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return JsonResponse(validateToken, validateToken['code'])  
  
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
                description="Admin Updated Successfully"
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
            if validateToken['user']['role'] == "ADMIN" :
                payload = request.data
                response, code = serviceAdmin.update(id, payload)
                return JsonResponse(response, status= code)
            else:
                return JsonResponse({"error": "You don't have access to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return JsonResponse(validateToken, validateToken['code'])  
          
    # @swagger_auto_schema(
    #     responses={
    #         200: openapi.Response(
    #             description="Admin Deleted Successfully"
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
    #         if validateToken['user']['role'] != "USER" :
    #             response, code = serviceAdmin.delete(id)
    #             return JsonResponse(response, status= code)
    #         else:
    #             return JsonResponse({"error": "You don't have access to perform this action."}, status=status.HTTP_403_FORBIDDEN)
    #     else:
    #         return JsonResponse(validateToken, validateToken['code'])   

class UserAdminChangePassword(APIView):
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
            if validateToken['user']['role'] == "ADMIN" :
                payload = request.data
                response, code = serviceAdmin.changePassword(id, payload)
                return JsonResponse(response, status= code)
            else:
                return JsonResponse({"error": "You don't have access to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return JsonResponse(validateToken, validateToken['code'])


class User(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'firstName': openapi.Schema(type=openapi.TYPE_STRING),
                'lastName': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD)
            },
            required=['firstName', 'lastName', 'email', 'password']
        ),
        responses={
            201: openapi.Response(
                description="User Created Successfully"
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
        validateToken = validateJwt(request.headers.get('Authorization'))
        if validateToken['status']:
            if(validateToken['user']['role'] == "ADMIN"):
                payload = request.data
                response,statusCode = serviceUser.createUser(payload)
                return JsonResponse(response, status=statusCode)
            else:
                return JsonResponse({"error": "You don't have access to perform this action."}, status=status.HTTP_403_FORBIDDEN)   
        else: 
            return JsonResponse(validateToken,status= validateToken['code']) 

    # @swagger_auto_schema(
    #     responses={
    #         200: openapi.Response(
    #             description="List of all  users",
    #         ),
    #         400: openapi.Response(
    #             description="Bad request"
    #         ),
    #          403: openapi.Response(
    #             description="Forbidden: You don't have access to perform this action."
    #         ),
    #         500: openapi.Response(
    #             description="Internal Server Error"
    #         )
    #     }
    # )
    # def get(self, request):
    #     validateToken = validateJwt(request.headers.get('Authorization'))
    #     if validateToken['status']:
    #         if(validateToken['user']['role'] == "ADMIN"):
    #             response,statusCode = serviceUser.getAllUsers()
    #             return JsonResponse(response, status=statusCode)
    #         else:
    #             return JsonResponse({"error": "You don't have access to perform this action."}, status=status.HTTP_403_FORBIDDEN)   
    #     else: 
    #         return JsonResponse(validateToken,status= validateToken['code'])   

class UserById(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="User Details"
            ),
            404: openapi.Response(
                description="Not Found"
            ),
            403: openapi.Response(
                description="Forbidden: You don't have access to perform this action."
            ),
            500: openapi.Response(
                description="Internal Server Error"
            )
        }
    )
    def get(self, request, id):
        validateToken = validateJwt(request.headers.get('Authorization'))
        if(validateToken['status']):
            if validateToken['user']['role'] != "SUPER_ADMIN" :
                response, code = serviceUser.getById(id)
                return JsonResponse(response, status= code)
            else:
                return JsonResponse({"error": "You don't have access to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return JsonResponse(validateToken, validateToken['code'])  
  
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
            if validateToken['user']['role'] == "ADMIN" :
                payload = request.data
                response, code = serviceUser.update(id, payload)
                return JsonResponse(response, status= code)
            else:
                return JsonResponse({"error": "You don't have access to perform this action."}, status=status.HTTP_403_FORBIDDEN)
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
            if validateToken['user']['role'] == "USER" :
                payload = request.data
                response, code = serviceUser.changePassword(id, payload)
                return JsonResponse(response, status= code)
            else:
                return JsonResponse({"error": "You don't have access to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return JsonResponse(validateToken, validateToken['code'])     
