from django.urls import path
from . import views
urlpatterns= [
    path('admin',views.UserAdmin.as_view(),name="admin"),
    path('admin/<str:id>',views.UserAdminById.as_view(),name="adminId"),
    path('admin/change-password/<str:id>',views.UserAdminChangePassword.as_view(),name="adminChangePaasword"),
    path('user',views.User.as_view(),name="user"),
    path('user/<str:id>',views.UserById.as_view(),name="userID"),
    path('user/change-password/<str:id>',views.UserChangePassword.as_view(),name="userChangePaasword"),
]