from rest_framework import serializers
from .models import PortalUser

class RegistrationSerializers(serializers.ModelSerializer):
    class Meta:
        model = PortalUser
        # fields = ['name','role','email','password']
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    role = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()
