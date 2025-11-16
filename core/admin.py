from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Position, TaskType, Worker, Task


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = (
        "last_name",
        "first_name",
        "username",
        "position",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    search_fields = ("username", "email", "first_name", "last_name")
    list_filter = ("position", "is_active", "is_staff", "is_superuser",)
    list_display_links = ("username",)
    list_select_related = ("position",)

    fieldsets = (
        (None, {"fields": ("username", "password",)}),
        ("Personal info", {
            "fields": ("first_name", "last_name", "email", "position",)
        }),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser",)
        }),
        ("Important dates", {
            "fields": ("last_login", "date_joined",), "classes": ("collapse",)
        }),
    )

    add_fieldsets = (
        (None, {
            "fields": (
                "username",
                "position",
                "first_name",
                "last_name",
                "email",
                "password1",
                "password2",
            ),
            "classes": ("wide",)
        }),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "task_type",
        "is_completed",
        "priority",
        "deadline",
        "get_assignees",
    )
    search_fields = ("name", "description",)
    list_filter = ("deadline", "is_completed", "priority", "task_type",)
    list_display_links = ("id", "name",)
    list_select_related = ("task_type",)
    list_editable = ("is_completed", "priority",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related("assignees")

    def get_assignees(self, obj):
        assignees = obj.assignees.all()
        if assignees:
            return ", ".join(
                [f"{w.first_name} {w.last_name}" for w in assignees]
            )
        return "No assignees"

    get_assignees.short_description = "Assignees"
