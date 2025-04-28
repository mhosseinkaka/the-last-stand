from rest_framework.serializers import ModelSerializer, StringRelatedField
from user.models import User
from rest_framework import serializers

class UserProfileSerializer(ModelSerializer):
    phone = StringRelatedField()
    first_name = StringRelatedField()
    last_name = StringRelatedField()
    role = StringRelatedField()
    class Meta:
        model = User
        fields = ['phone', 'first_name', 'last_name', 'role']
        read_only_fields = ['phone', 'role']

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserListSerializer(ModelSerializer):
    phone = StringRelatedField()
    first_name = StringRelatedField()
    last_name = StringRelatedField()
    role = StringRelatedField()
    class Meta:
        model = User
        fields = ['phone', 'first_name', 'last_name', 'role', 'is_active', 'is_staff']
        read_only_fields = ['phone', 'role']


class SendOTPSerializer(ModelSerializer):
    phone = serializers.CharField(max_length=11)

class VerifyOTPSerializer(ModelSerializer):
    phone = serializers.CharField(max_length=11)
    code = serializers.CharField(max_length=6)

class LoginSerializer(ModelSerializer):
    phone = serializers.CharField()
    password = serializers.CharField()

class SetPasswordSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, min_length=6)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def save(self, user):
        user.set_password(self.validated_data['password'])
        user.save()
        return user