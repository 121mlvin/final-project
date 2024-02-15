from rest_framework import serializers, validators
from django.contrib.auth.models import User
from tasksapp.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class RegistrarionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')

        extra_kwargs = {
            'password': {'write_only': True},
            'email': {
                'required': True,
                'allow_blank': False,
                'validators':[
                    validators.UniqueValidator(
                        User.objects.all(), 'This email already registered'
                    )
                ]
            }
        }
    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')

        user = User.objects.create(
            username=username,
            password=password,
            email=email
        )
        return user
