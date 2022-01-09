from rest_framework import serializers
from .models import UserInteraction
import requests
from environ import Env

env = Env()


class UserInteractionSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserInteraction
        fields = ['user_id', 'content_id', 'is_like', 'is_read']

    def validate_user_id(self, user_id):
        user_response = requests.get(f"{env('USER_URL')}/users/{user_id}")
        if user_response.status_code != 200:
            raise serializers.ValidationError("invalid id")
        return user_id

    def validate_content_id(self, content_id):
        content_response = requests.get(f"{env('CONTENT_URL')}/books/{content_id}")
        if content_response.status_code != 200:
            raise serializers.ValidationError("invalid id")
        return content_id

    def update(self, instance, validated_data):
        if instance.is_read:
            validated_data.pop('is_read', None)
        return super(UserInteractionSerializer, self).update(instance, validated_data)