from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
from blog.models import BlogPost, BlogImage
from blog.serializers import BlogPostSerializer, BlogImageSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from user.permissions import IsSupportUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.core.exceptions import PermissionDenied
# Create your views here.

class BlogPostListView(ListAPIView):
    queryset = BlogPost.objects.filter(published=True).order_by('-publish_date')
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'tags', 'published']
    search_fields = ['author','title', 'subtitle', 'body']
    ordering_fields = ['publish_date', 'title', 'date_modified']
    ordering = ['-publish_date']  

class BlogPostDetailView(RetrieveAPIView):
    queryset = BlogPost.objects.filter(published=True)
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]


class BlogPostCreateView(CreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated, IsSupportUser]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class BlogPostUpdateView(UpdateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated, IsSupportUser]


class BlogPostDeleteView(DestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated, IsSupportUser]


class BlogImageUploadView(CreateAPIView):
    serializer_class = BlogImageSerializer
    permission_classes = [IsAuthenticated, IsSupportUser]

    def perform_create(self, serializer):
        # اجازه بده نویسنده فقط روی پست خودش عکس بزاره
        blog = serializer.validated_data['blog']
        if blog.author != self.request.user:
            raise PermissionDenied("اجازه بارگذاری برای این پست را ندارید.")
        serializer.save()