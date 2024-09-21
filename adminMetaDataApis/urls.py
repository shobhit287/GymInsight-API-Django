from django.urls import path,include
from . import views
urlpatterns=[
   path('admin-meta-data',views.AdminMetaData.as_view(),name="adminMeta")
]