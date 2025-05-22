from django.contrib import admin
from blog.models import BlogPost, BlogImage, Tag
# Register your models here.

admin.site.register(BlogPost)
admin.site.register(BlogImage)
admin.site.register(Tag)