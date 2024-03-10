from .models import CustomerUser
from phonenumber_field.serializerfields import PhoneNumberField

from rest_framework import serializers


class UserCreationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=30)
    email = serializers.EmailField(max_length=100)
    phone_number = PhoneNumberField(allow_null=False, allow_blank=False)
    password = serializers.CharField(min_length=8)

    class Meta:
        model = CustomerUser
        fields = ['username', 'email', 'phone_number', 'password']

    def validate(self, attrs):
        username = CustomerUser.objects.filter(
            username=attrs['username']
        ).exists()

        if username:
            raise serializers.ValidationError(detail='username exist')
        
        email = CustomerUser.objects.filter(
            email=attrs['email']
        ).exists()

        if email:
            raise serializers.ValidationError(detail='email exist')
        
        phone_number = CustomerUser.objects.filter(
            phone_number=attrs['phone_number']
        ).exists()

        if phone_number:
            raise serializers.ValidationError(detail='phone_number exist')
        
        return super().validate(attrs)