from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            'full_name', 'email', 'phone', 'address',
            'project_title', 'supervisor', 'cycle'
        ]
