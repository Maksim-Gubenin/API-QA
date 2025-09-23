from typing import ClassVar, List

from rest_framework import serializers

from .models import Answer, Question


class AnswerSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Answer."""

    user_id: serializers.UUIDField = serializers.UUIDField(required=True)

    class Meta:
        """Метаданные сериализатора Answer."""

        model: ClassVar[type[Answer]] = Answer
        fields: ClassVar[List[str]] = [
            "id",
            "question_id",
            "user_id",
            "text",
            "created_at",
        ]
        read_only_fields: ClassVar[List[str]] = ["id", "created_at"]


class QuestionListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка вопросов (только ID и текст)."""

    class Meta:
        """Метаданные сериализатора списка вопросов."""

        model: ClassVar[type[Question]] = Question
        fields: ClassVar[List[str]] = ["id", "text"]
        read_only_fields: ClassVar[List[str]] = ["id"]


class QuestionDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детального просмотра вопроса (все поля + ответы)."""

    answers: AnswerSerializer = AnswerSerializer(many=True, read_only=True)

    class Meta:
        """Метаданные сериализатора детального просмотра вопроса."""

        model: ClassVar[type[Question]] = Question
        fields: ClassVar[List[str]] = ["id", "text", "created_at", "answers"]
        read_only_fields: ClassVar[List[str]] = ["id", "created_at"]


class AnswerCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания ответа."""

    user_id: serializers.UUIDField = serializers.UUIDField(required=True)

    class Meta:
        """Метаданные сериализатора создания ответа."""

        model: ClassVar[type[Answer]] = Answer
        fields: ClassVar[List[str]] = ["user_id", "text"]
