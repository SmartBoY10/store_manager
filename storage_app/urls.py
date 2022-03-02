from django.urls import path
from .views import *

urlpatterns = [
    path('', ManualView.as_view(), name='storage_home'),
    path('manual/<int:pk>/', ManualDetailView.as_view(), name='manual_detail')
]