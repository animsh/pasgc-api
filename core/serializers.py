from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import UserGradeAnalysisData, UserCareerAnalysisData

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = '__all__'


class UserGradeAnalysisDataSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserGradeAnalysisData
        fields = '__all__'


class UserCareerAnalysisDataSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserCareerAnalysisData
        fields = '__all__'
