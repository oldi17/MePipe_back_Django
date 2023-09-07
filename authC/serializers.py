import os
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import UnsupportedMediaType

from .models import User
from .utils import saveImage1x1
import MePipe.settings as settings


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return user

class UserModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    logo = serializers.ImageField(write_only=True, allow_empty_file=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'logo')
    
    def create(self, validated_data):
        file = validated_data.pop('logo', None)
        try:
            saveImage1x1(file.file, os.path.join(settings.MEDIA_ROOT_PFP, validated_data['username'] + '.png'))
        except:
            raise UnsupportedMediaType('', detail='Loaded profile picture is not of supported format(png, jpeg, webp)')
        user = User.objects.create_user(**validated_data)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        file = validated_data.pop('logo', None)
        if file:
            try:
                saveImage1x1(file.file, os.path.join(settings.MEDIA_ROOT_PFP, instance.username + '.png'))
            except:
                raise UnsupportedMediaType('', detail='Loaded profile picture is not of supported format(png, jpeg, webp)')

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance