from django.urls import path
from user.views import UserListView, CreateNormalUserView, UserProfileView, SendOTPView, VerifyOTPView, CreateSupportUserView

urlpatterns = [
    path('user-list/', UserListView.as_view()),
    path('create-user/', CreateNormalUserView.as_view()),
    path('admin-user/', CreateSupportUserView.as_view()),
    path('edit-profile/<int:pk>/', UserProfileView.as_view()),
    path('send-otp/', SendOTPView.as_view()),
    path('verify-otp/', VerifyOTPView.as_view()),
]