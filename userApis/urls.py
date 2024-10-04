from django.urls import path
from . import views
urlpatterns= [
    path('user',views.User.as_view(),name="user"),
    path('user/<str:id>',views.UserById.as_view(),name="userID"),
    path('user/change-password/<str:id>',views.UserChangePassword.as_view(),name="userChangePaasword"),
]