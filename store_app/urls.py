from django.urls import path
from .views import *

urlpatterns = [
    path('', get_list, name='home'),
]
