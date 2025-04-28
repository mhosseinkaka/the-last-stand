from django.urls import path
from bootcamp.views import BootcampListCreateView, BootcampRetrieveUpdateDestroyView

urlpatterns = [
    path('create-bootcamp/', BootcampListCreateView.as_view(), name='bootcamp-list-create'),
    path('bootcamp/<int:pk>/', BootcampRetrieveUpdateDestroyView.as_view(), name='bootcamp-detail'),
]