from django.contrib.auth.models import User
from django import forms
from .models import *
from .models import Movie



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']



class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title','genre', 'description','year', 'movie_logo']
        
        
        
class RatingForm(forms.ModelForm):
    class Meta:
        model = Myrating
        fields = ['rating']