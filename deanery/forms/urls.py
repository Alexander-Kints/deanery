from django.urls import path

from .views import *

urlpatterns = [
    path('create/', FormCreateAPIView.as_view()),
    path('get/<int:form_id>/', FormGetAPIView.as_view()),
]
