from django.urls import path,include
from . import views
urlpatterns=[
   path('admin-meta-data',views.AdminMetaData.as_view(),name="adminMeta"),
   path('admin-meta-data/<str:id>',views.AdminMetaDataById.as_view(),name="adminMetaById"),
   path('admin-meta-data/<str:id>/approve',views.AdminMetaDataApprove.as_view(),name="adminMetaApprove"),
   path('admin-meta-data/<str:id>/reject',views.AdminMetaDataReject.as_view(),name="adminMetaReject"),
]