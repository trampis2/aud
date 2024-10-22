from django.urls import path
from .views import manage_group_permissions

urlpatterns = [
    path('manage_roles/', manage_group_permissions, name='manage_roles'),
]