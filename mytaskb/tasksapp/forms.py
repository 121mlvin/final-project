from django import forms
from django.contrib.auth.models import User
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['creator', 'performer', 'text']

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(TaskForm, self).__init__(*args, **kwargs)

        if request:
            if request.user.is_superuser:
                self.fields['creator'].queryset = User.objects.filter(pk=request.user.pk)
                self.fields['performer'].queryset = User.objects.all()
            else:
                self.fields['creator'].queryset = User.objects.filter(pk=request.user.pk)
                self.fields['performer'].queryset = User.objects.filter(pk=request.user.pk)


class ChangeStatus(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"


class ChangeText(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['text']
