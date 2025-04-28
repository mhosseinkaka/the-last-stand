from rest_framework.serializers import ModelSerializer, StringRelatedField
from bootcamp.models import Bootcamp, BootcampCategory


class BootcampCategorySerializer(ModelSerializer):
    class Meta:
        model = BootcampCategory
        fields = '__all__'

class BootcampSerializer(ModelSerializer):
    class Meta:
        model = Bootcamp
        fields = '__all__'


class BootcampViewSerializer(ModelSerializer):
    title = StringRelatedField()
    category = StringRelatedField()
    price = StringRelatedField()
    start_date = StringRelatedField()
    end_date = StringRelatedField()
    student_count = StringRelatedField()
    location = StringRelatedField()
    class Meta:
        model = Bootcamp
        fields = ['title', 'category', 'price', 'start_date', 'end_date', 'student_count', 'location']