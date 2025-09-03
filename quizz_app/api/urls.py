from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TranscribeView, QuizViewset

router = DefaultRouter()
router.register(r'quizzes', QuizViewset, basename='quiz')

urlpatterns = router.urls + [
    path('createQuiz/', TranscribeView.as_view(), name='create_quiz'),
]