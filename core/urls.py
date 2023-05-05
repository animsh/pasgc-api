from django.urls import path, include
from .views import UserGradeAnalysisDataView, UserCareerAnalysisDataView, UserGradeAnalysisDataListView, UserCareerAnalysisDataListView, UserGradeAnalysisResultView, UserCareerAnalysisResultView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("user_grade_analysis_data/", UserGradeAnalysisDataListView.as_view()),
    path("user_grade_analysis_data/<int:enrollment_number>/",
         UserGradeAnalysisDataView.as_view()),
    path("user_career_analysis_data/",
         UserCareerAnalysisDataListView.as_view()),
    path("user_career_analysis_data/<int:enrollment_number>/",
         UserCareerAnalysisDataView.as_view()),

    path("user_grade_analysis_result/<int:enrollment_number>/",
         UserGradeAnalysisResultView.as_view()),
    path("user_career_analysis_result/<int:enrollment_number>/",
         UserCareerAnalysisResultView.as_view()),
]
