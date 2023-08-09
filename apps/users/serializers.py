from rest_framework import serializers
from .models import CustomUser

class RegisterUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username','email', 'password',)
    

    def validate_email(self, email):
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email already exists")
        return email

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user