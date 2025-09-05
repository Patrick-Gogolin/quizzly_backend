from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
import os, json
from .services import download_audio, transcribe_audio, generate_quiz
from .serializers import QuizRequestSerializer, QuizResponsePostSerializer, QuizResponseRetrieveUpdateSerializer
from ..models import Quiz, Question
from .permissions import IsOwner

class TranscribeView(generics.CreateAPIView):
    serializer_class = QuizRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        url = serializer.validated_data['url']

        audio_file = None

        try: 
            audio_file = download_audio(url)

            transcript = transcribe_audio(audio_file)

            generated_quiz = generate_quiz(transcript)
            generated_quiz_data = json.loads(generated_quiz)

            quiz = Quiz.objects.create(
                user=request.user,
                title=generated_quiz_data['title'],
                description=generated_quiz_data['description'],
                video_url=url
            )

            for question in generated_quiz_data['questions']:
                Question.objects.create(
                    quiz=quiz,
                    question_title=question['question_title'],
                    question_options=question['question_options'],
                    answer=question['answer']
                )
            
            response_serializer = QuizResponsePostSerializer(quiz)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        finally:
            if audio_file and os.path.exists(audio_file):
                os.remove(audio_file)

class ListQuizzesView(generics.ListAPIView):
    serializer_class = QuizResponseRetrieveUpdateSerializer
    
    def get_queryset(self):
        return Quiz.objects.filter(user=self.request.user)

class QuizViewset(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Quiz.objects.all()
    serializer_class = QuizResponseRetrieveUpdateSerializer

    def get_queryset(self):
        if self.action == "list":
            return Quiz.objects.filter(user=self.request.user)
        elif self.action in ["retrieve", "destroy", "update", "partial_update"]:
            return Quiz.objects.all()