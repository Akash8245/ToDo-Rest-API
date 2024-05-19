from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User,Task


class UserSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ['name','email','password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)
        return user

class TaskSerializer(serializers.ModelSerializer):
    class Meta():
        model = Task
        fields = '__all__'