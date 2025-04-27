
from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from user.models import User, OTP
from user.serializers import UserSerializer, UserProfileSerializer, UserListSerializer, SendOTPSerializer, VerifyOTPSerializer
from user.permissions import IsSuperUser, IsSupportUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
import random
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from kavenegar import *
from django.contrib.auth.models import Group



# Create your views here.

class UserListView(ListAPIView):
    permission_classes = [IsSuperUser, IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['last_name', 'first_name', 'role', 'is_active']
    search_fields = ['role']
    
class CreateSupportUserView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsSuperUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()

        try:
            support_group = Group.objects.get(name='Supports')
            user.groups.add(support_group)
        except Group.DoesNotExist:
            raise Exception("گروه Supports پیدا نشد. لطفاً گروه را ایجاد کنید.")

        user.role = 'support'
        user.is_staff = True
        user.save()

class CreateNormalUserView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsSupportUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserProfileView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

class SendOTPView(APIView):
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']

        recent = OTP.objects.filter(phone=phone).order_by('-created_at').first()
        if recent and recent.created_at > timezone.now() - timedelta(seconds=90):
            return Response({"detail": "کد اخیراً ارسال شده، لطفاً کمی صبر کنید."}, status=429)

        code = str(random.randint(100000, 999999))
        OTP.objects.create(phone=phone, code=code)
        try:
            api = KavenegarAPI('484C7571326A3573413549737736714853344858424A39364F6A4B5A724F70594C38396C6F5755517262593D')
            params = { 'sender' : '2000660110', 'receptor': phone, 'message' :f"کد تایید شما : {code}" }
            api.sms_send(params)
        except (APIException, HTTPException) as e:
            print("Kavenegar error:", e)
            return Response({"detail": "ارسال پیامک با مشکل مواجه شد."}, status=400)

        return Response({"detail": "کد تأیید ارسال شد."})


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        code = serializer.validated_data['code']

        otp_qs = OTP.objects.filter(phone=phone, code=code).order_by('-created_at')
        if not otp_qs.exists() or not otp_qs.first().is_valid():
            return Response({"detail": "کد اشتباه یا منقضی شده."}, status=400)

        user, created = User.objects.get_or_create(phone=phone)

        if created:
            try:
                student_group = Group.objects.get(name='Students')
                user.groups.add(student_group)
            except Group.DoesNotExist:
                return Response({"detail": "گروه Students پیدا نشد. لطفاً ابتدا گروه را بسازید."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'is_new_user': created
        })