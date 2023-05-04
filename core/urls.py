from django.urls import path, include
from .views import UserGradeAnalysisDataView, UserCareerAnalysisDataView, UserGradeAnalysisDataListView, UserCareerAnalysisDataListView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("user_grade_analysis_data/", UserGradeAnalysisDataListView.as_view()),
    path("user_grade_analysis_data/<int:enrollment_number>/",
         UserGradeAnalysisDataView.as_view()),
    path("user_career_analysis_data/",
         UserCareerAnalysisDataListView.as_view()),
    path("user_career_analysis_data/<int:enrollment_number>/",
         UserCareerAnalysisDataView.as_view()),
]
