from django import forms
from django.forms import widgets 
from . models import *

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title','description']

class DataInput(forms.DateInput):
    input_type = 'date'

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due':DataInput()}
        fields = ['subject','title','description','due','is_finished']

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','is_finished']

class DashboardForm(forms.Form):
     text = forms.CharField(max_length=100,label="Enter your search: ")
