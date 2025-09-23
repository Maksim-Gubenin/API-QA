from typing import ClassVar

from django.db import models


class Question(models.Model):
    """Модель вопроса."""

    class Meta:
        """Метаданные модели Question."""

        verbose_name: ClassVar[str] = "Вопрос"
        verbose_name_plural: ClassVar[str] = "Вопросы"
        ordering: ClassVar[list[str]] = ["-created_at"]

    text: models.TextField = models.TextField(verbose_name="Текст вопроса", blank=False)
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания вопроса",
    )

    def __str__(self) -> str:
        """Строковое представление вопроса."""
        if len(self.text) > 50:
            return f"Вопрос #{self.id}: {self.text[:50]}..."
        return f"Вопрос #{self.id}: {self.text}"


class Answer(models.Model):
    """Модель ответа на вопрос."""

    class Meta:
        """Метаданные модели Answer."""

        verbose_name: ClassVar[str] = "Ответ"
        verbose_name_plural: ClassVar[str] = "Ответы"
        ordering: ClassVar[list[str]] = ["created_at"]
        indexes: ClassVar[list[models.Index]] = [
            models.Index(fields=["user_id"]),
        ]

    question_id: models.ForeignKey = models.ForeignKey(
        to=Question,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name="Ответ",
    )
    user_id: models.UUIDField = models.UUIDField(
        verbose_name="ID пользователя",
        editable=False,
    )
    text: models.TextField = models.TextField(verbose_name="Текст ответа")
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания ответа",
    )

    def __str__(self) -> str:
        """Строковое представление ответа."""
        return f"Ответ #{self.id} к вопросу #{self.question_id}"
