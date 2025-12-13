from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    TemplateView,
)

from core.models import Task, TaskType
from core.forms import TaskForm, TaskSearchForm, TaskFilterForm

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
            "urgent": tasks.filter(priority="urgent",
                                   is_completed=False).count(),
            "high": tasks.filter(priority="high", is_completed=False).count(),
            "medium": tasks.filter(priority="medium",
                                   is_completed=False).count(),
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

        # Search filter
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(description__icontains=search)
            )

        # Status filter
        status = self.request.GET.get("status")
        if status == "completed":
            queryset = queryset.filter(is_completed=True)
        elif status == "pending":
            queryset = queryset.filter(is_completed=False)

        # Priority filter
        priority = self.request.GET.get("priority")
        if priority and priority != "all":
            queryset = queryset.filter(priority=priority)

        # Task type filter
        task_type_id = self.request.GET.get("task_type")
        if task_type_id and task_type_id != "all":
            queryset = queryset.filter(task_type_id=task_type_id)

        # Deadline filter
        deadline_filter = self.request.GET.get("deadline_filter")
        today = timezone.now().date()
        if deadline_filter:
            if deadline_filter == "today":
                queryset = queryset.filter(deadline=today)
            elif deadline_filter == "next_3_days":
                end_date = today + timezone.timedelta(days=3)
                queryset = queryset.filter(deadline__gte=today,
                                           deadline__lte=end_date)
            elif deadline_filter == "next_week":
                end_date = today + timezone.timedelta(days=7)
                queryset = queryset.filter(deadline__gte=today,
                                           deadline__lte=end_date)
            elif deadline_filter == "overdue":
                queryset = queryset.filter(deadline__lt=today,
                                           is_completed=False)

        # Assignee filter
        assignee_id = self.request.GET.get("assignee")
        if assignee_id and assignee_id != "all":
            queryset = queryset.filter(assignees__id=assignee_id).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_page"] = "active"
        context["today"] = timezone.now().date()

        search_form = TaskSearchForm(self.request.GET)
        filter_form = TaskFilterForm(self.request.GET)

        context["search_form"] = search_form
        context["filter_form"] = filter_form

        active_filters_count = 0
        filter_data = filter_form.data if filter_form.is_bound else {}

        if filter_data.get("deadline_filter") and filter_data.get(
                "deadline_filter") != "all":
            active_filters_count += 1
        if filter_data.get("status") and filter_data.get("status") != "all":
            active_filters_count += 1
        if filter_data.get("priority") and filter_data.get(
                "priority") != "all":
            active_filters_count += 1
        if filter_data.get("task_type") and filter_data.get(
                "task_type") != "all":
            active_filters_count += 1
        if filter_data.get("assignee") and filter_data.get(
                "assignee") != "all":
            active_filters_count += 1

        context["active_filters_count"] = active_filters_count
        context["has_active_filters"] = active_filters_count > 0

        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("core:task-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_page"] = "active"
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("core:task-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_page"] = "active"
        context["today"] = timezone.now().date()
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
