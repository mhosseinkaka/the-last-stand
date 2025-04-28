from django.urls import path
from user.views import UserListView, CreateNormalUserView, UserProfileView, SendOTPView, VerifyOTPView, CreateSupportUserView, PasswordLoginView, SetPasswordView

urlpatterns = [
    path('user-list/', UserListView.as_view(), name='user-list'),
    path('create-user/', CreateNormalUserView.as_view(), name='create-user'),
    path('admin-user/', CreateSupportUserView.as_view(), name='admin-user'),
    path('edit-profile/<int:pk>/', UserProfileView.as_view(), name='edit-profile'),
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('password-login/', PasswordLoginView.as_view(), name='password-login'),
    path('set-password/', SetPasswordView.as_view(), name='set-password'),
]