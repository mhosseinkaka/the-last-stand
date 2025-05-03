from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from blog.models import BlogPost, Tag, BlogImage

class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class BlogImageSerializer(ModelSerializer):
    class Meta:
        model = BlogImage
        fields = ['id', 'image', 'caption']

class BlogPostSerializer(ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    tags = TagSerializer(many=True, required=False)
    images = BlogImageSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'subtitle', 'slug', 'body', 'meta_description',
            'date_created', 'date_modified', 'publish_date', 'published',
            'author', 'tags', 'images'
        ]

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        blog = BlogPost.objects.create(**validated_data)
        for tag in tags_data:
            tag_obj, _ = Tag.objects.get_or_create(name=tag['name'])
            blog.tags.add(tag_obj)
        return blog