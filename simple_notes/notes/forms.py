from django import forms
from .models import Notebook, Note, Profile
from django.contrib.auth.models import User


class NotebookForm(forms.ModelForm):
    class Meta:
        model = Notebook
        fields = ['title']


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['language', 'theme']
