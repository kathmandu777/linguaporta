import re

from django.contrib import admin

from ..models import Question, Unit


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    fields = ("number", "text", "answer", "created_at")
    ordering = ("number",)
    readonly_fields = ("created_at",)


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    inlines = (QuestionInline,)

    list_display = (
        "id",
        "name",
        "questions_count",
        "category_name",
        "range_start",
        "range_end",
        "created_at",
    )
    search_fields = ("name",)
    # ordering = ("category_name", "range_start")

    def questions_count(self, obj: Unit) -> int:
        return Question.objects.filter(unit=obj).count()

    def category_name(self, obj: Unit) -> str:
        return re.sub(r"\(\d+-\d+\)", "", obj.name)

    def range_start(self, obj: Unit) -> int:
        return int(re.findall(r"\((\d+)-\d+\)", obj.name)[0])

    def range_end(self, obj: Unit) -> int:
        return int(re.findall(r"\(\d+-(\d+)\)", obj.name)[0])
