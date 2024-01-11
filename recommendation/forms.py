from django import forms
from django.forms import ModelForm
from django.forms import widgets 
from . models import *
from django.contrib.auth.forms import UserCreationForm

class UsersRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']
        help_texts={
    'username': None,
}

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title','description']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter your course title then enter a number from 1 to 5'}),
            'description': forms.Textarea(attrs={'placeholder': '                                                     Enter your feedback description(How it helped you and How we can enhance it)'}),
        }

class SidForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['SID']

class DataInput(forms.DateInput):
    input_type = 'date'

class DashboardForm(forms.Form):
     text = forms.CharField(max_length=100,label="Enter your search: ")

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['stars']
        widgets = {
            'stars': forms.RadioSelect(attrs={'class': 'star-rating'})
        }