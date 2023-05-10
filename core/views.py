from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserGradeAnalysisDataSerializer, UserCareerAnalysisDataSerializer
from .models import UserGradeAnalysisData, UserCareerAnalysisData
from rest_framework.response import Response
from rest_framework import status
from .utils.career_prediction import inputlist
from .utils.grade_prediction import convert_to_csv, predict_grade
from rest_framework.exceptions import ValidationError, NotAuthenticated, APIException, AuthenticationFailed, NotFound


class UserGradeAnalysisDataListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserGradeAnalysisDataSerializer
    queryset = UserGradeAnalysisData.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            response = {
                'status': 'success',
                'message': 'Grade analysis data retrieved successfully',
                'data': data
            }
            return Response(response, status=status.HTTP_200_OK)
        except APIException as e:
            response = {
                'status': 'error',
                'message': 'An error occurred while retrieving grade analysis data',
                'detail': str(e)
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        updateRequest = request
        updateRequest.data['user_id'] = request.user.id
        updateRequest.data['enrollment_number'] = request.user.enrollment_number
        serializer = self.get_serializer(data=updateRequest.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({
                'status': 'error',
                'message': 'Validation error',
                'errors': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=request.user)
        data = serializer.data
        status_code = status.HTTP_201_CREATED
        response = {
            'status': 'success',
            'message': 'Grade analysis data created successfully',
            'data': data
        }
        return Response(response, status=status_code)

    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            response = {
                'status': 'error',
                'message': 'Validation error',
                'errors': exc.detail
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        elif isinstance(exc, NotAuthenticated):
            response = {
                'status': 'error',
                'message': 'Authentication credentials were not provided'
            }
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        elif isinstance(exc, AuthenticationFailed):
            return Response({
                'status': 'error',
                'message': 'Authentication failed'
            }, status=status.HTTP_401_UNAUTHORIZED)
        elif isinstance(exc, NotFound):
            response = {
                'status': 'error',
                'message': 'Requested resource not found'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        response = {
            'status': 'error',
            'message': 'An error occurred while retrieving/updating/deleting data',
            'detail': str(exc)
        }
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserGradeAnalysisDataView(CreateAPIView, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserGradeAnalysisDataSerializer
    queryset = UserGradeAnalysisData.objects.all()
    lookup_field = 'enrollment_number'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            response = {
                'status': 'error',
                'message': 'Validation error',
                'errors': e.detail
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=request.user)
        data = serializer.data
        response = {
            'status': 'success',
            'message': 'Grade analysis data created successfully',
            'data': data
        }
        return Response(response, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            data = serializer.data
            response = {
                'status': 'success',
                'message': 'Grade analysis data retrieved successfully',
                'data': data
            }
            return Response(response, status=status.HTTP_200_OK)
        except APIException as e:
            response = {
                'status': 'error',
                'message': 'An error occurred while retrieving grade analysis data',
                'detail': str(e)
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        updateRequest = request
        updateRequest.data['user_id'] = request.user.id
        updateRequest.data['enrollment_number'] = request.user.enrollment_number
        serializer = self.get_serializer(data=updateRequest.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            response = {
                'status': 'error',
                'message': 'Validation error',
                'errors': e.detail
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=request.user)
        data = serializer.data
        response = {
            'status': 'success',
            'message': 'Grade analysis data created successfully',
            'data': data
        }
        return Response(response, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        updateRequest = request
        updateRequest.data['user_id'] = request.user.id
        updateRequest.data['enrollment_number'] = request.user.enrollment_number
        serializer = self.get_serializer(
            instance, data=updateRequest.data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            response = {
                'status': 'error',
                'message': 'Validation error',
                'errors': e.detail
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        data = serializer.data
        response = {
            'status': 'success',
            'message': 'Grade analysis data updated successfully',
            'data': data
        }
        return Response(response, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            response = {
                'status': 'success',
                'message': 'Grade analysis data deleted successfully'
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)
        except APIException as e:
            response = {
                'status': 'error',
                'message': 'An error occurred while deleting grade analysis data',
                'detail': str(e)
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            response = {
                'status': 'error',
                'message': 'Validation error',
                'errors': exc.detail
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        elif isinstance(exc, NotAuthenticated):
            response = {
                'status': 'error',
                'message': 'Authentication credentials were not provided'
            }
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        elif isinstance(exc, AuthenticationFailed):
            return Response({
                'status': 'error',
                'message': 'Authentication failed'
            }, status=status.HTTP_401_UNAUTHORIZED)
        elif isinstance(exc, NotFound):
            response = {
                'status': 'error',
                'message': 'Requested resource not found'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        response = {
            'status': 'error',
            'message': 'An error occurred while retrieving/updating/deleting data',
            'detail': str(exc)
        }
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserCareerAnalysisDataListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserCareerAnalysisDataSerializer
    queryset = UserCareerAnalysisData.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            response = {
                'status': 'success',
                'message': 'Career analysis data retrieved successfully',
                'data': data
            }
            return Response(response, status=status.HTTP_200_OK)
        except APIException as e:
            response = {
                'status': 'error',
                'message': 'An error occurred while retrieving career analysis data',
                'detail': str(e)
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            response = {
                'status': 'error',
                'message': 'Validation error',
                'errors': e.detail
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=request.user)
        data = serializer.data
        response = {
            'status': 'success',
            'message': 'Career analysis data created successfully',
            'data': data
        }
        return Response(response, status=status.HTTP_201_CREATED)

    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            response = {
                'status': 'error',
                'message': 'Validation error',
                'errors': exc.detail
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        elif isinstance(exc, NotAuthenticated):
            response = {
                'status': 'error',
                'message': 'Authentication credentials were not provided'
            }
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        elif isinstance(exc, AuthenticationFailed):
            return Response({
                'status': 'error',
                'message': 'Authentication failed'
            }, status=status.HTTP_401_UNAUTHORIZED)
        elif isinstance(exc, NotFound):
            response = {
                'status': 'error',
                'message': 'Requested resource not found'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        response = {
            'status': 'error',
            'message': 'An error occurred while retrieving/updating/deleting data',
            'detail': str(exc)
        }
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserCareerAnalysisDataView(CreateAPIView, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserCareerAnalysisDataSerializer
    queryset = UserCareerAnalysisData.objects.all()
    lookup_field = 'enrollment_number'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            data = serializer.data
            response = {
                'status': 'success',
                'message': 'Career analysis data retrieved successfully',
                'data': data
            }
            return Response(response, status=status.HTTP_200_OK)
        except APIException as e:
            response = {
                'status': 'error',
                'message': 'An error occurred while retrieving career analysis data',
                'detail': str(e)
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            response = {
                'status': 'error',
                'message': 'Validation error',
                'errors': e.detail
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=request.user)
        data = serializer.data
        response = {
            'status': 'success',
            'message': 'Career analysis data created successfully',
            'data': data
        }
        return Response(response, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = serializer.data
            response = {
                'status': 'success',
                'message': 'Career analysis data updated successfully',
                'data': data
            }
            return Response(response, status=status.HTTP_200_OK)
        except ValidationError as e:
            response = {
                'status': 'error',
                'message': 'Validation error',
                'errors': e.detail
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except APIException as e:
            response = {
                'status': 'error',
                'message': 'An error occurred while updating career analysis data',
                'detail': str(e)
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            response = {
                'status': 'success',
                'message': 'Career analysis data deleted successfully'
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)
        except APIException as e:
            response = {
                'status': 'error',
                'message': 'An error occurred while deleting career analysis data',
                'detail': str(e)
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            response = {
                'status': 'error',
                'message': 'Validation error',
                'errors': exc.detail
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        elif isinstance(exc, NotAuthenticated):
            response = {
                'status': 'error',
                'message': 'Authentication credentials were not provided'
            }
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        elif isinstance(exc, AuthenticationFailed):
            return Response({
                'status': 'error',
                'message': 'Authentication failed'
            }, status=status.HTTP_401_UNAUTHORIZED)
        elif isinstance(exc, NotFound):
            response = {
                'status': 'error',
                'message': 'Requested resource not found'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        response = {
            'status': 'error',
            'message': 'An error occurred while retrieving/updating/deleting data',
            'detail': str(exc)
        }
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserGradeAnalysisResultView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserGradeAnalysisDataSerializer
    queryset = UserGradeAnalysisData.objects.all()
    lookup_field = 'enrollment_number'

    def get(self, request, *args, **kwargs):
        if kwargs.get('enrollment_number') != request.user.enrollment_number:
            return Response({
                "status": "error",
                "message": "You are not authorized to view this data.",
            }, status=status.HTTP_403_FORBIDDEN)

        gradeData = UserGradeAnalysisData.objects.filter(
            enrollment_number=kwargs.get('enrollment_number')).first()

        if not gradeData:
            return Response({
                "status": "error",
                "message": "No data found.",
            }, status=status.HTTP_404_NOT_FOUND)

        name, subjects = convert_to_csv(gradeData)
        first, second, third, fourth, fifth, sixth = predict_grade(name)

        response_data = {
            'status': 'success',
            'message': 'Grade analysis result retrieved successfully',
            'data': {
                'first': first,
                'second': second,
                'third': third,
                'fourth': fourth,
                'fifth': fifth,
                'sixth': sixth,
                'subjects': subjects
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            response = {
                'status': 'error',
                'message': 'Validation error',
                'errors': exc.detail
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        elif isinstance(exc, NotAuthenticated):
            response = {
                'status': 'error',
                'message': 'Authentication credentials were not provided'
            }
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        elif isinstance(exc, AuthenticationFailed):
            return Response({
                'status': 'error',
                'message': 'Authentication failed'
            }, status=status.HTTP_401_UNAUTHORIZED)
        elif isinstance(exc, NotFound):
            response = {
                'status': 'error',
                'message': 'Requested resource not found'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        response = {
            'status': 'error',
            'message': 'An error occurred while retrieving/updating/deleting data',
            'detail': str(exc)
        }
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserCareerAnalysisResultView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserCareerAnalysisDataSerializer
    queryset = UserCareerAnalysisData.objects.all()
    lookup_field = 'enrollment_number'

    def get(self, request, *args, **kwargs):
        if kwargs.get('enrollment_number') != request.user.enrollment_number:
            return Response({
                "status": "error",
                "message": "You are not authorized to view this data.",
            }, status=status.HTTP_403_FORBIDDEN)

        gradeData = UserCareerAnalysisData.objects.filter(
            enrollment_number=kwargs.get('enrollment_number'))

        if not gradeData:
            return Response({
                "status": "error",
                "message": "No data found.",
            }, status=status.HTTP_404_NOT_FOUND)

        try:
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
        except Exception as e:
            return Response({
                "status": "error",
                "message": "An error occurred while processing the data.",
                "detail": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "status": "success",
            "message": "Career analysis result retrieved successfully.",
            "data": result
        }, status=status.HTTP_200_OK)

    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            response = {
                'status': 'error',
                'message': 'Validation error',
                'errors': exc.detail
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        elif isinstance(exc, NotAuthenticated):
            response = {
                'status': 'error',
                'message': 'Authentication credentials were not provided'
            }
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        elif isinstance(exc, AuthenticationFailed):
            return Response({
                'status': 'error',
                'message': 'Authentication failed'
            }, status=status.HTTP_401_UNAUTHORIZED)
        elif isinstance(exc, NotFound):
            response = {
                'status': 'error',
                'message': 'Requested resource not found'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        response = {
            'status': 'error',
            'message': 'An error occurred while retrieving/updating/deleting data',
            'detail': str(exc)
        }
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
