from django.urls import path
from .views import TranscribeView, ListQuizzesView


urlpatterns = [
    path('createQuiz/', TranscribeView.as_view(), name='create_quiz'),
    path('quizzes/', ListQuizzesView.as_view(), name='list_quizzes')
]