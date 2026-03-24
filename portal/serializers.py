from rest_framework import serializers
from .models import PortalUser,Tasks

class RegistrationSerializers(serializers.ModelSerializer):
    class Meta:
        model = PortalUser
        # fields = ['name','role','email','password']
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    role = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()

class TaskSerializer(serializers.ModelSerializer):
    assigned_by = serializers.CharField(source='assigned_by.name')
    assigned_to = serializers.CharField(source='assigned_to.name')

    class Meta:
        model = Tasks
        fields = '__all__'