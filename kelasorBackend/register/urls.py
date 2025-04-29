from django.urls import path
from register.views import RegisterBootcampView, RegistrationListView, RegistrationStatusUpdateView, CancelRegistrationView


urlpatterns = [
    path('bootcamp/<int:bootcamp_id>/register/', RegisterBootcampView.as_view(), name='bootcamp-register'),
    path('pending-registrations/', RegistrationListView.as_view(), name='pending-registrations'),
    path('update-registration/<int:pk>/', RegistrationStatusUpdateView.as_view(), name='update-registration'),
    path('cancel-registration/<int:pk>/', CancelRegistrationView.as_view(), name='cancel-registration'),
]