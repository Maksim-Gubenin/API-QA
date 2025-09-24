import uuid

from django.test import TestCase

from api_qa.models import Answer, Question


class QuestionModelTest(TestCase):
    """Тесты для модели Question."""

    def test_question_creation(self) -> None:
        """Тестирует создание вопроса."""
        question: Question = Question.objects.create(text="Test question?")
        self.assertEqual(question.text, "Test question?")
        self.assertIsNotNone(question.created_at)

    def test_question_str_method(self) -> None:
        """Тестирует метод __str__ для модели Question."""
        question: Question = Question.objects.create(
            text="{0}l{1}".format("s" * 49, "S" * 30)
        )

        self.assertIn("l...", str(question))
        self.assertNotIn("S", str(question))

        short_question: Question = Question.objects.create(text="Короткий вопрос")
        expected_short_str: str = f"Вопрос #{short_question.id}: Короткий вопрос"
        self.assertEqual(str(short_question), expected_short_str)


class AnswerModelTest(TestCase):
    """Тесты для модели Answer."""

    def setUp(self) -> None:
        """Подготовка данных для тестов."""
        self.question: Question = Question.objects.create(text="Test question?")
        self.user_id: uuid.UUID = uuid.uuid4()

    def test_answer_creation(self) -> None:
        """Тестирует создание ответа."""
        answer: Answer = Answer.objects.create(
            question_id=self.question, user_id=self.user_id, text="Test answer"
        )
        self.assertEqual(answer.text, "Test answer")
        self.assertEqual(answer.question_id, self.question)
        self.assertEqual(answer.user_id, self.user_id)

    def test_answer_str_method(self) -> None:
        """Тестирует метод __str__ для модели Answer."""
        answer: Answer = Answer.objects.create(
            question_id=self.question, user_id=self.user_id, text="Test answer"
        )

        expected_str: str = f"Ответ #{answer.id} к вопросу #{self.question}"
        self.assertEqual(str(answer), expected_str)
