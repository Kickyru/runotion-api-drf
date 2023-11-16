from rest_framework import serializers

from user.models import UserProfile


class PreviewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'image']
