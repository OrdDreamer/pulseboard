from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    View,
    TemplateView,
)

from core.models import Task

User = get_user_model()


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        today = timezone.now().date()
        tasks = Task.objects.all()

        total_tasks = tasks.count()
        completed_tasks = tasks.filter(is_completed=True).count()
        pending_tasks = tasks.filter(is_completed=False).count()
        overdue_tasks = tasks.filter(
            is_completed=False,
            deadline__lt=today
        ).count()

        my_tasks = tasks.filter(
            assignees=user,
            is_completed=False
        ).select_related("task_type").prefetch_related("assignees")

        upcoming_deadline = today + timezone.timedelta(days=7)
        upcoming_tasks = my_tasks.filter(
            deadline__lt=upcoming_deadline,
            deadline__gte=today
        ).order_by("deadline")

        urgent_tasks = my_tasks.filter(priority__in=["urgent", "high"])

        priority_stats = {
            "urgent": tasks.filter(priority="urgent", is_completed=False).count(),
            "high": tasks.filter(priority="high", is_completed=False).count(),
            "medium": tasks.filter(priority="medium", is_completed=False).count(),
            "low": tasks.filter(priority="low", is_completed=False).count(),
        }

        context.update({
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "overdue_tasks": overdue_tasks,
            "my_tasks": my_tasks[:10],
            "upcoming_tasks": upcoming_tasks[:5],
            "urgent_tasks": urgent_tasks[:5],
            "priority_stats": priority_stats,
            "dashboard_page": "active",
        })

        return context


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "core/task_list.html"
    context_object_name = "tasks"
    paginate_by = 20

    def get_queryset(self):
        queryset = Task.objects.select_related(
            "task_type"
        ).prefetch_related(
            "assignees"
        )

        status = self.request.GET.get("status")
        if status == "completed":
            queryset = queryset.filter(is_completed=True)
        elif status == "pending":
            queryset = queryset.filter(is_completed=False)

        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(description__icontains=search)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_page"] = "active"
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_page"] = "active"
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_page"] = "active"
        return context


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_page"] = "active"
        return context


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_page"] = "active"
        return context


class WorkerListView(LoginRequiredMixin, ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["worker_page"] = "active"
        return context


class WorkerDetailView(LoginRequiredMixin, DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["worker_page"] = "active"
        return context


class WorkerUpdateView(LoginRequiredMixin, UpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["worker_page"] = "active"
        return context
