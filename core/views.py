from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserGradeAnalysisDataSerializer, UserCareerAnalysisDataSerializer
from .models import UserGradeAnalysisData, UserCareerAnalysisData


class UserGradeAnalysisDataListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserGradeAnalysisDataSerializer
    queryset = UserGradeAnalysisData.objects.all()


class UserGradeAnalysisDataView(CreateAPIView, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserGradeAnalysisDataSerializer
    queryset = UserGradeAnalysisData.objects.all()
    lookup_field = 'enrollment_number'


class UserCareerAnalysisDataListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserCareerAnalysisDataSerializer
    queryset = UserCareerAnalysisData.objects.all()


class UserCareerAnalysisDataView(CreateAPIView, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserCareerAnalysisDataSerializer
    queryset = UserCareerAnalysisData.objects.all()
    lookup_field = 'enrollment_number'
