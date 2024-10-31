from django.urls import path
from .views import *

urlpatterns = [
    path('<int:form_id>/', show_form),
    path('create/', create_form),
    path('list/', form_list),
]
