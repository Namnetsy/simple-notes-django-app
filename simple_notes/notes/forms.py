from django import forms
from .models import Notebook, Note

class NotebookForm(forms.ModelForm):
    class Meta:
        model = Notebook
        fields = ['title']

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
