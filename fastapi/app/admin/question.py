from django.contrib import admin

from ..models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "unit",
        "number",
        "text",
        "answer",
        "created_at",
    )
    search_fields = ("number", "text", "answer")
    list_filter = ("unit",)
    ordering = ("unit", "number")
