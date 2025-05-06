from rest_framework.permissions import IsAuthenticated
from user.permissions import IsSupportUser
from register.models import Registration
from register.serializers import RegisterSerializer, RegisterStatusUpdateSerializer
from bootcamp.models import Bootcamp
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
import http.client
import json

# Create your views here.

class RegisterBootcampView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        bootcamp_id = self.kwargs.get('bootcamp_id')
        try:
            bootcamp = Bootcamp.objects.get(id=bootcamp_id)
        except Bootcamp.DoesNotExist:
            return Response({"detail": "بوتکمپ مورد نظر یافت نشد."}, status=status.HTTP_404_NOT_FOUND)
        
        if bootcamp.status != 'open':
            return Response({"detail": "ثبت‌نام در این بوتکمپ امکان‌پذیر نیست."}, status=status.HTTP_400_BAD_REQUEST)

        if bootcamp.student_count >= bootcamp.capacity:
            return Response({"detail": "ظرفیت بوتکمپ تکمیل شده است."}, status=status.HTTP_400_BAD_REQUEST)

        if Registration.objects.filter(student=request.user, bootcamp=bootcamp).exists():
            return Response({"detail": "شما قبلاً در این بوتکمپ ثبت‌نام کرده‌اید."}, status=status.HTTP_400_BAD_REQUEST)

        registration = Registration.objects.create(student=request.user, bootcamp=bootcamp)
        serializer = self.get_serializer(registration)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RegistrationListView(ListAPIView):
    permission_classes = [IsAuthenticated, IsSupportUser]
    queryset = Registration.objects.filter(status='pending')
    serializer_class = RegisterSerializer
    

class RegistrationStatusUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsSupportUser]
    queryset = Registration.objects.all()
    serializer_class = RegisterStatusUpdateSerializer
    

    def perform_update(self, serializer):
        registration = self.get_object()
        previous_status = registration.status
        updated_registration = serializer.save()

        if previous_status == 'pending' and updated_registration.status == 'approved':
            bootcamp = updated_registration.bootcamp
            bootcamp.student_count += 1
            bootcamp.save()

            phone = updated_registration.student.phone
            message = f"ثبت‌نام شما در بوتکمپ {bootcamp.title} تایید شد."
            conn = http.client.HTTPSConnection("api.sms.ir")
            payload = json.dumps({
                                "lineNumber": 30002108001178,
                                "messageText": message,
                                "mobiles": [phone],      
                                })
            headers = {
                'X-API-KEY': '...',
                'Content-Type': 'application/json'}
            conn.request("POST", "/v1/send/bulk", payload, headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))


class CancelRegistrationView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Registration.objects.all()
    serializer_class = RegisterSerializer
    

    def update(self, request, *args, **kwargs):
        registration = self.get_object()

        if registration.student != request.user:
            return Response({"detail": "شما اجازه لغو این ثبت‌نام را ندارید."}, status=status.HTTP_403_FORBIDDEN)

        if registration.status not in ['pending', 'approved']:
            return Response({"detail": "امکان لغو این وضعیت وجود ندارد."}, status=status.HTTP_400_BAD_REQUEST)

        if registration.status == 'approved' and registration.bootcamp.student_count > 0:
            registration.bootcamp.student_count -= 1
            registration.bootcamp.save()

        registration.status = 'cancelled'
        registration.save()

        return Response({"detail": "ثبت‌نام با موفقیت لغو شد."}, status=status.HTTP_200_OK)
