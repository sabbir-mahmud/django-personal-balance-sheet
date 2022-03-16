# imports
from django import forms
from .models import Todo_list

# add/edit task form


class TaskForm(forms.ModelForm):
    class Meta:
        model = Todo_list
        fields = '__all__'
        exclude = ['done']
        labels = {'title': 'Task Title'}
        widgets = {'title': forms.TextInput(
            attrs={'class': 'form-control', 'id': 'form'})}
