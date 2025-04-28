from django.urls import path
from bootcamp.views import BootcampCreateView, BootcampRetrieveUpdateDestroyView, BootcampAdminListView, BootcampListView

urlpatterns = [
    path('create-bootcamp/', BootcampCreateView.as_view(), name='bootcamp-list-create'),
    path('bootcamp/<int:pk>/', BootcampRetrieveUpdateDestroyView.as_view(), name='bootcamp-detail'),
    path('bootcamp-admin-list/', BootcampAdminListView.as_view(), name='bootcamp-admin-list'),
    path('bootcamp-list/', BootcampListView.as_view(), name='bootcamp-list'),
]