from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Position Name"
    )

    class Meta:
        verbose_name = "Position"
        verbose_name_plural = "Positions"
        ordering = ["name"]

    def __str__(self):
        return self.name


class TaskType(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Task Type Name",
    )

    class Meta:
        verbose_name = "Task Type"
        verbose_name_plural = "Task Types"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Position",
        related_name="workers"
    )

    class Meta:
        verbose_name = "Worker"
        verbose_name_plural = "Workers"
        ordering = [
            "last_name",
            "first_name",
            "username"
        ]

    def __str__(self):
        first_name = self.first_name or "N/A"
        last_name = self.last_name or "N/A"
        position = self.position.name if self.position else "N/A"

        return f"{first_name} {last_name} ({self.username}) - {position}"


class Task(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Task Name"
    )
    description = models.TextField(
        verbose_name="Task Description"
    )
    deadline = models.DateField(
        verbose_name="Task Deadline"
    )
    is_completed = models.BooleanField(
        default=False,
        verbose_name="Is Completed"
    )
    priority = models.CharField(
        max_length=255,
        choices=[
            ("urgent", "Urgent"),
            ("high", "High"),
            ("medium", "Medium"),
            ("low", "Low"),
        ],
        default="medium",
        verbose_name="Task Priority"
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Task Type",
        related_name="tasks"
    )
    assignees = models.ManyToManyField(
        Worker,
        blank=True,
        verbose_name="Assigned To",
        related_name="tasks"
    )

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ["-id"]

    def __str__(self):
        task_type_str = self.task_type.name if self.task_type else "N/A"
        return f"{self.name} [{self.priority}] - {task_type_str}"
