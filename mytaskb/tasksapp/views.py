from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DeleteView

from .models import Task
from .forms import TaskForm, ChangeStatus, ChangeText


@method_decorator(login_required, name='dispatch')
class TasksList(ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.all()


@login_required
def change_status(request, task_id, direction):
    task = get_object_or_404(Task, id=task_id)
    current_status_index = Task.STATUS_CHOICES.index((task.status, task.status))

    if (
            not task.status_changed
            and (
            (not request.user.is_superuser and request.user == task.performer and current_status_index < 3)
            or (request.user.is_superuser and task.status == 'Ready')
    )
    ):
        if direction == 'left' and current_status_index > 0:
            task.status = Task.STATUS_CHOICES[current_status_index - 1][0]
            task.status_changed = True
        elif direction == 'right' and current_status_index < len(Task.STATUS_CHOICES) - 1:
            task.status = Task.STATUS_CHOICES[current_status_index + 1][0]
            task.status_changed = True
        task.save()

    form = ChangeStatus(instance=task)

    if request.method == 'POST':
        form = ChangeStatus(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('change_status')

    return render(request, 'change_status.html', {'task': task, 'form': form})


@login_required
def edit_text(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.user == task.creator:
        form = ChangeText(request.POST or None, instance=task)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = None

    return render(request, 'edit_text.html', {'task': task, 'form': form})


@login_required
def create_task(request):
    form = TaskForm(request=request)

    if request.method == 'POST':
        form = TaskForm(request.POST, request=request)

        if form.is_valid():
            form.save()
            return redirect('task_list')

    return render(request, 'create_task.html', {'form': form})


@staff_member_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list')


