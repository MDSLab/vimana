from django import forms
from .models import MLModel

class MLModelForm(forms.ModelForm):
    class Meta:
        model = MLModel
        fields = ('title', 'description', 'accuracy', 'file', )
