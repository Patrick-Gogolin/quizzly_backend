from rest_framework import serializers
from ..models import Quiz, Question

QUESTION_BASE_SERIALIZER_FIELDS = ['id', 'question_title', 'question_options', 'answer', 'created_at', 'updated_at']
QUESTION_LEAN_FIELDS = ['id', 'question_title', 'question_options', 'answer']

def validate_youtube_url(value: str) -> str:
        if "youtube.com/watch?v=" in value :
            video_id = value.split("v=")[1]
        elif "youtu.be/" in value:
            video_id = value.split("youtu.be/")[1].split("?")[0]
        else:
            raise serializers.ValidationError("Invalid Youtube URL format.")
        return f"https://www.youtube.com/watch?v={video_id}"

class QuizRequestSerializer(serializers.Serializer):
    url = serializers.URLField(required=True)

    def validate_url(self, value):
        return validate_youtube_url(value)

class QuestionBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = QUESTION_BASE_SERIALIZER_FIELDS

class QuestionLeanSerializer(QuestionBaseSerializer):
    class Meta(QuestionBaseSerializer.Meta):
        fields = QUESTION_LEAN_FIELDS

class QuizBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'video_url', 'questions']
    
    def validate_video_url(self, value):
        return validate_youtube_url(value)

class QuizResponsePostSerializer(QuizBaseSerializer):
    questions = QuestionBaseSerializer(many=True, read_only=True)

class QuizResponseRetrieveUpdateSerializer(QuizBaseSerializer):
    questions = QuestionLeanSerializer(many=True, read_only=True)