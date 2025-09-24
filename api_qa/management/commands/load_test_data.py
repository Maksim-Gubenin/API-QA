from typing import Any

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Команда для загрузки тестовых данных в базу данных."""

    help: str = "Загружает тестовые данные в базу данных"

    def handle(self, *args: Any, **options: Any) -> None:
        """
        Основной метод выполнения команды.

        Загружает фикстуры questions.json и answers.json в базу данных.
        """
        self.stdout.write("Загрузка тестовых данных...")

        call_command("loaddata", "questions.json", app_label="api_qa")
        call_command("loaddata", "answers.json", app_label="api_qa")

        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно загружены!"))
