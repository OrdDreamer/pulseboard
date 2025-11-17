from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from core.models import Task

User = get_user_model()


@login_required
def index(request):
    user = request.user
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

    context = {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "overdue_tasks": overdue_tasks,
        "my_tasks": my_tasks[:10],
        "upcoming_tasks": upcoming_tasks[:5],
        "urgent_tasks": urgent_tasks[:5],
        "priority_stats": priority_stats,
    }

    return render(request, "core/index.html", context)


class TaskListView(ListView):
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


class TaskCreateView(CreateView):
    pass


class TaskDetailView(DetailView):
    pass


class TaskUpdateView(UpdateView):
    pass


class TaskDeleteView(DeleteView):
    pass


class WorkerListView(ListView):
    pass


class WorkerDetailView(DetailView):
    pass


class WorkerUpdateView(UpdateView):
    pass
