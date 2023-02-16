from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "important"]

        # add styles css
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Write a title..."}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control mt-1",
                    "placeholder": "Write a description...",
                }
            ),
            "important": forms.CheckboxInput(attrs={"class": "form-check-input mt-1"}),
        }
