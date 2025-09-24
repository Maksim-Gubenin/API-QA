import uuid
from typing import Any, Dict

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api_qa.models import Answer, Question


class QuestionAPITest(APITestCase):
    """Тесты API для модели Question."""

    def setUp(self) -> None:
        """Подготовка данных для тестов вопросов."""
        self.question: Question = Question.objects.create(text="Test question?")
        self.list_url: str = reverse("question-list")
        self.detail_url: str = reverse(
            "question-detail", kwargs={"pk": self.question.id}
        )

    def test_get_questions_list(self) -> None:
        """Тестирует получение списка вопросов."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_questions_list_serializer(self) -> None:
        """Тестирует, что список вопросов возвращает только ID и текст."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        question_data: Dict[str, Any] = response.data["results"][0]
        self.assertIn("id", question_data)
        self.assertIn("text", question_data)
        self.assertNotIn("created_at", question_data)
        self.assertNotIn("answers", question_data)

    def test_create_question(self) -> None:
        """Тестирует создание нового вопроса."""
        data: Dict[str, str] = {"text": "New question?"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 2)

    def test_get_question_detail(self) -> None:
        """Тестирует получение детальной информации о вопросе."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["text"], self.question.text)
        self.assertIn("created_at", response.data)
        self.assertIn("answers", response.data)

    def test_delete_question(self) -> None:
        """Тестирует удаление вопроса."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Question.objects.count(), 0)


class AnswerAPITest(APITestCase):
    """Тесты API для модели Answer."""

    def setUp(self) -> None:
        """Подготовка данных для тестов ответов."""
        self.question: Question = Question.objects.create(text="Test question?")
        self.user_id: uuid.UUID = uuid.uuid4()
        self.answer: Answer = Answer.objects.create(
            question_id=self.question, user_id=self.user_id, text="Test answer"
        )
        self.create_url: str = reverse(
            "answer-create", kwargs={"question_id": self.question.id}
        )
        self.detail_url: str = reverse("answer-detail", kwargs={"pk": self.answer.id})

    def test_create_answer(self) -> None:
        """Тестирует создание нового ответа."""
        data: Dict[str, str] = {"user_id": str(uuid.uuid4()), "text": "New answer"}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Answer.objects.count(), 2)

    def test_get_answer_detail(self) -> None:
        """Тестирует получение детальной информации об ответе."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["text"], self.answer.text)

    def test_delete_answer(self) -> None:
        """Тестирует удаление ответа."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Answer.objects.count(), 0)

    def test_cascade_delete(self) -> None:
        """Тестирует каскадное удаление ответов при удалении вопроса."""
        Answer.objects.create(
            question_id=self.question, user_id=uuid.uuid4(), text="Another answer"
        )

        question_url: str = reverse("question-detail", kwargs={"pk": self.question.id})
        response = self.client.delete(question_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Answer.objects.count(), 0)

    def test_cannot_create_answer_to_nonexistent_question(self) -> None:
        """Тестирует попытку создания ответа для несуществующего вопроса."""
        data: Dict[str, str] = {
            "user_id": str(uuid.uuid4()),
            "text": "Answer to nonexistent question",
        }
        response = self.client.post(
            reverse("answer-create", kwargs={"question_id": 999}), data
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
