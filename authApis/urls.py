from django.urls import path
from . import views
urlpatterns= [
    path('auth/login',views.Auth.as_view(),name="login"),
    path('auth/forget-password',views.AuthForgetPassword.as_view(),name="forgetPassword"),
    path('auth/verify-reset-token/<str:token>',views.AuthVerifyToken.as_view(),name="verifyResetToken"),
    path('auth/reset-password/<str:token>',views.AuthResetPassword.as_view(),name="resetPassword"),
]