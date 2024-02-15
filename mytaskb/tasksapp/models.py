from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In progress', 'In progress'),
        ('In QA', 'In QA'),
        ('Ready', 'Ready'),
        ('Done', 'Done'),
    ]

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    performer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='performed_tasks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    status_changed = models.BooleanField(default=False)
    text = models.TextField()

    def __str__(self):
        return f'{self.creator}, {self.performer}, {self.status}, {self.text}'
