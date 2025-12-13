from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import (
    password_validators_help_text_html
)
from django.utils.safestring import mark_safe

from core.models import Task, TaskType, Position

User = get_user_model()


class WorkerCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "position",
            "email",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        rules = password_validators_help_text_html()
        self.fields["password1"].help_text = mark_safe(
            f"<div class='password-rules'>{rules}</div>"
        )
        self.fields["first_name"].widget.attrs.update({"autofocus": True})
        self.fields["username"].widget.attrs.pop("autofocus", None)


class TaskSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Search by name or description...",
        })
    )


class TaskFilterForm(forms.Form):
    DEADLINE_CHOICES = [
        ("all", "All"),
        ("today", "Today"),
        ("next_3_days", "Next 3 days"),
        ("next_week", "Next week"),
        ("overdue", "Overdue"),
    ]

    STATUS_CHOICES = [
        ("all", "All"),
        ("completed", "Completed"),
        ("pending", "Pending"),
    ]

    PRIORITY_CHOICES = [
        ("all", "All"),
        ("urgent", "Urgent"),
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    ]

    deadline_filter = forms.ChoiceField(
        choices=DEADLINE_CHOICES,
        required=False,
        initial="all",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        initial="all",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    priority = forms.ChoiceField(
        choices=PRIORITY_CHOICES,
        required=False,
        initial="all",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    task_type = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={"class": "form-select"})
    )

    assignee = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={"class": "form-select"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        task_type_choices = [("all", "All")]
        task_type_choices.extend([
            (str(type.id), type.name) for type in
            TaskType.objects.all().order_by("name")
        ])
        self.fields["task_type"].choices = task_type_choices

        assignee_choices = [("all", "All")]
        for worker in User.objects.all().order_by("username"):
            if worker.first_name or worker.last_name:
                display_name = (f"{worker.first_name}"
                                f" {worker.last_name}".strip())
            else:
                display_name = worker.username
            assignee_choices.append((str(worker.id), display_name))
        self.fields["assignee"].choices = assignee_choices


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "assignees": forms.CheckboxSelectMultiple(),
            "deadline": forms.DateInput(attrs={"type": "date"})
        }


class WorkerSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Search by name, surname, or username...",
        })
    )


class WorkerFilterForm(forms.Form):
    position = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={"class": "form-select"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        position_choices = [("all", "All")]
        position_choices.extend([
            (str(pos.id), pos.name)
            for pos in Position.objects.all().order_by("name")
        ])
        self.fields["position"].choices = position_choices
