from django.contrib import admin

from .models import Answer, Question


class AnswerInline(admin.TabularInline):
    """Inline для отображения ответов в админке вопроса."""

    model = Answer
    extra = 0
    max_num = 0
    can_add = False
    readonly_fields = ["user_id_short", "text_short", "created_at"]

    def user_id_short(self, obj):
        return str(obj.user_id)[:8]

    user_id_short.short_description = "User ID"

    def text_short(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text

    text_short.short_description = "Текст"

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Админка для модели Question."""

    list_display = ["id", "text_short", "answers_count", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["text"]
    inlines = [AnswerInline]

    def text_short(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text

    text_short.short_description = "Текст вопроса"

    def answers_count(self, obj):
        return obj.answers.count()

    answers_count.short_description = "Ответы"


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """Админка для модели Answer."""

    list_display = ["id", "question_id", "user_id_short", "text_short", "created_at"]
    list_filter = ["created_at", "question_id"]
    search_fields = ["text"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def text_short(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text

    text_short.short_description = "Текст ответа"

    def user_id_short(self, obj):
        return str(obj.user_id)[:8]

    user_id_short.short_description = "User ID"
