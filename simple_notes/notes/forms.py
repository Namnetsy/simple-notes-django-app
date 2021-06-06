from django import forms
from django.utils.translation import get_language

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


class UserAccountForm(forms.ModelForm):
    password2 = forms.CharField(max_length=200, required=True)  # TODO: validate this field

    def save(self, commit=True):
        user = super(forms.ModelForm, self).save(commit=False)
        user.save()
        self.save_m2m()

        Profile(user=user, language=get_language()).save()

        return user

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
