import logging
from typing import Any, Type

from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from .models import Answer, Question
from .serializers import (
    AnswerCreateSerializer,
    AnswerSerializer,
    QuestionDetailSerializer,
    QuestionListSerializer,
)

logger = logging.getLogger(__name__)


class QuestionListCreateView(generics.ListCreateAPIView):
    """View для получения списка вопросов и создания нового вопроса."""

    queryset = Question.objects.all()

    def get_serializer_class(self) -> Type[Serializer]:
        """
        Возвращает класс сериализатора в зависимости от метода запроса.

        Returns:
            QuestionListSerializer для GET запросов (список)
            QuestionDetailSerializer для POST запросов (создание)
        """

        if self.request.method == "GET":
            return QuestionListSerializer
        return QuestionDetailSerializer

    def perform_create(self, serializer: Serializer) -> None:
        """Логирует создание нового вопроса."""

        instance: Question = serializer.save()
        logger.info(f"Created question #{instance.id}: {instance.text[:50]}...")


class QuestionDetailView(generics.RetrieveDestroyAPIView):
    """View для получения детальной информации о вопросе и его удаления."""

    queryset = Question.objects.all()
    serializer_class: Type[Serializer] = QuestionDetailSerializer

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Обрабатывает GET запрос для получения вопроса."""

        instance: Question = self.get_object()
        serializer: Serializer = self.get_serializer(instance)
        logger.info(f"Retrieved question #{instance.id}")
        return Response(serializer.data)

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Обрабатывает DELETE запрос для удаления вопроса."""

        instance: Question = self.get_object()
        question_id: int = instance.id
        self.perform_destroy(instance)
        logger.info(f"Deleted question #{question_id} with all its answers")
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnswerCreateView(generics.CreateAPIView):
    """View для создания ответа на конкретный вопрос."""

    queryset = Answer.objects.all()
    serializer_class: Type[Serializer] = AnswerCreateSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Создает новый ответ для указанного вопроса."""

        question_id = kwargs.get("question_id")
        question: Question = get_object_or_404(Question, id=question_id)

        serializer: Serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        answer: Answer = Answer.objects.create(
            question_id=question,
            user_id=serializer.validated_data["user_id"],
            text=serializer.validated_data["text"],
        )

        logger.info(
            f"User {answer.user_id} created answer "
            f"#{answer.id} for question #{question_id}"
        )

        response_serializer: AnswerSerializer = AnswerSerializer(answer)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class AnswerDetailView(generics.RetrieveDestroyAPIView):
    """View для получения и удаления конкретного ответа."""

    queryset = Answer.objects.all()
    serializer_class: Type[Serializer] = AnswerSerializer

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Обрабатывает GET запрос для получения ответа."""
        instance: Answer = self.get_object()
        serializer: Serializer = self.get_serializer(instance)
        logger.info(f"Retrieved answer #{instance.id}")
        return Response(serializer.data)

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Обрабатывает DELETE запрос для удаления ответа."""
        instance: Answer = self.get_object()
        answer_id: int = instance.id
        self.perform_destroy(instance)
        logger.info(f"Deleted answer #{answer_id}")
        return Response(status=status.HTTP_204_NO_CONTENT)
