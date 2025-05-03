from django.urls import path
from blog.views import BlogPostCreateView, BlogPostListView, BlogPostUpdateView, BlogPostDeleteView, BlogPostDetailView


urlpatterns = [
    path('', BlogPostListView.as_view(), name='blog-list'),
    path('<slug:slug>/', BlogPostDetailView.as_view(), name='blog-detail'),
    path('create/', BlogPostCreateView.as_view(), name='blog-create'),
    path('<int:pk>/update/', BlogPostUpdateView.as_view(), name='blog-update'),
    path('<int:pk>/delete/', BlogPostDeleteView.as_view(), name='blog-delete'),
]