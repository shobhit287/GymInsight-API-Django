from django.urls import path
from . import views
urlpatterns=[
    path('fees-renewal',views.FeesRenewal.as_view(),name="feesRenewal"),
    path('fees-renewal/<str:id>',views.FeesRenewalById.as_view(),name="userMetaDataById"),
]