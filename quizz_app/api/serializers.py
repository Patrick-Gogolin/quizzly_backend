from rest_framework import serializers
from ..models import Quiz, Question

class QuizRequestSerializer(serializers.Serializer):
    url = serializers.URLField(required=True)

    def validate_url(self, value):
        if "youtube.com/watch?v=" in value :
            video_id = value.split("v=")[1]
        elif "youtu.be/" in value:
            video_id = value.split("youtu.be/")[1].split("?")[0]
        else:
            raise serializers.ValidationError("Invalid Youtube URL format.")
        return f"https://www.youtube.com/watch?v={video_id}"

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_title', 'question_options', 'answer', 'created_at', 'updated_at']

class QuizResponseSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'video_url', 'questions']