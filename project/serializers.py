from rest_framework import serializers

from project.models import Project
from user.serializers import PreviewUserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    admin = PreviewUserSerializer()

    class Meta:
        model = Project
        fields = ['id', 'name', 'admin', 'image']


class PreviewProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'image']
