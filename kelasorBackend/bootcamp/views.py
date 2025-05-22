from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from bootcamp.models import Bootcamp
from bootcamp.serializers import BootcampSerializer, BootcampViewSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from bootcamp.permissions import *
from user.permissions import IsSuperUser, IsSupportUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
# Create your views here.

class BootcampCreateView(CreateAPIView):
    permission_classes = [IsSuperUser | IsAdminUser]
    queryset = Bootcamp.objects.all()
    serializer_class = BootcampSerializer
    

class BootcampRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSuperUser | IsAdminUser]
    queryset = Bootcamp.objects.all()
    serializer_class = BootcampSerializer
    

class BootcampAdminListView(ListAPIView):
    permission_classes = [IsSuperUser | IsAdminUser]
    queryset = Bootcamp.objects.all()
    serializer_class = BootcampSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['title', 'category', 'price', 'location', 'status', 'start_date', 'end_date']
    search_fields = ['title', 'price', 'start_date', 'end_date', 'location']


class BootcampListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Bootcamp.objects.all()
    serializer_class = BootcampViewSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['title', 'category', 'price', 'student_count', 'location']
    search_fields = ['title', 'price', 'start_date', 'end_date', 'location']   