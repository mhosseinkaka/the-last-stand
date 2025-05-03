from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
# Create your models here.

User = get_user_model()

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    slug = models.SlugField(unique=True, blank=True) #url
    body = models.TextField()
    meta_description = models.CharField(max_length=160, blank=True) #seo
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(null=True, blank=True)
    published = models.BooleanField(default=False)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    

class BlogImage(models.Model):
    blog = models.ForeignKey(to=BlogPost, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.blog.title}"