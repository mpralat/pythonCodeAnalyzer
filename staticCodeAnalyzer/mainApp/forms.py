from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('repository_url',)


class ProjectHiddenForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('repository_url',)
