from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserGradeAnalysisDataSerializer, UserCareerAnalysisDataSerializer
from .models import UserGradeAnalysisData, UserCareerAnalysisData
from rest_framework.response import Response
from rest_framework import status
from .utils.career_prediction import inputlist


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


class UserGradeAnalysisResultView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserGradeAnalysisDataSerializer
    queryset = UserGradeAnalysisData.objects.all()
    lookup_field = 'enrollment_number'


class UserCareerAnalysisResultView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserCareerAnalysisDataSerializer
    queryset = UserCareerAnalysisData.objects.all()
    lookup_field = 'enrollment_number'

    def get(self, request, *args, **kwargs):
        if kwargs.get('enrollment_number') != request.user.enrollment_number:
            return Response({'error': 'You are not authorized to view this data.'}, status=status.HTTP_403_FORBIDDEN)

        gradeData = UserCareerAnalysisData.objects.filter(
            enrollment_number=kwargs.get('enrollment_number'))

        if not gradeData:
            return Response({'error': 'No data found.'}, status=status.HTTP_404_NOT_FOUND)

        result = inputlist(gradeData[0].user.name,
                           gradeData[0].enrollment_number,
                           gradeData[0].user.email,
                           gradeData[0].logical_quotient_rating,
                           gradeData[0].coding_skills_rating,
                           gradeData[0].hackathons,
                           gradeData[0].public_speaking_points,
                           gradeData[0].self_learning_capability,
                           gradeData[0].extra_courses_did,
                           gradeData[0].taken_inputs_from_seniors_or_elders,
                           gradeData[0].worked_in_teams_ever,
                           gradeData[0].introvert,
                           gradeData[0].reading_writing_skills,
                           gradeData[0].memory_capability_score,
                           gradeData[0].hard_or_smart_worker,
                           gradeData[0].management_or_technical,
                           gradeData[0].interested_subjects,
                           gradeData[0].interested_type_of_books,
                           gradeData[0].certifications,
                           gradeData[0].workshops,
                           gradeData[0].type_of_company_want_to_settle_in,
                           gradeData[0].interested_career_area)

        return Response(result, status=status.HTTP_200_OK)
