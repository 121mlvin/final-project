from django.urls import path
from . import views

urlpatterns = [
    path('', views.TasksList.as_view(), name='task_list'),
    path('create/', views.create_task, name='create_task'),
    path('change-status/<int:task_id>/<str:direction>', views.change_status, name='change_status'),
    path('edit/<int:task_id>/', views.edit_text, name='edit_text'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
]