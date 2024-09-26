from django.urls import path
from . import views
urlpatterns=[
    path('user-meta-data',views.UserMetaData.as_view(),name="userMetaData"),
    path('user-meta-data/<str:id>',views.UserMetaDataById.as_view(),name="userMetaDataById"),
]