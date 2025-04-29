from rest_framework.serializers import ModelSerializer, ValidationError
from register.models import Registration

class RegisterSerializer(ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'
        read_only_fields = ['status', 'registered_at']

class RegisterStatusUpdateSerializer(ModelSerializer):
    class Meta:
        model = Registration
        fields = ['status']

    def validate_status(self, value):
        if value not in ['approved', 'rejected']:
            raise ValidationError("وضعیت باید تاییدشده یا ردشده باشد.")
        return value