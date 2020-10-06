from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import auth_login
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .forms import NotebookForm, NoteForm
from .models import Notebook, Note


def index(request):
    if request.user.is_authenticated:
        notebooks = Notebook.objects.filter(user=request.user)

        return render(request, 'notes/home.html', {'notebooks': notebooks})
    
    return render(request, 'notes/index.html')


@login_required
def view_notes(request, notebook_title):
    notebook = Notebook.objects.get(user=request.user, title=notebook_title)
    notes = Note.objects.filter(notebook=notebook)

    context = {
        'notes': notes,
        'notebook_title': notebook_title,
    }

    return render(request, 'notes/view-notes.html', context)


@login_required
def edit_note(request, notebook_title, note_title):
    notebook = Notebook.objects.get(user=request.user, title=notebook_title)
    note = Note.objects.get(notebook=notebook, title=note_title)
    form = NoteForm(instance=note)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)

        if form.is_valid():
            note = form.save(commit=False)
            note.modified_at = timezone.now()
            note.save()

            return redirect('notes:index')
    
    context = {
        'form': form,
        'notebook_title': notebook_title,
        'note_title': note_title,
    }

    return render(request, 'notes/edit-note.html', context)


@login_required
def create_note(request, title):
    form = NoteForm()

    if request.method == 'POST':
        form = NoteForm(request.POST)

        if form.is_valid():
            notebook = Notebook.objects.get(user=request.user, title=title)
            note = form.save(commit=False)
            note.notebook = notebook
            note.save()

            return redirect(reverse('notes:view-notes', args=[title]))

    return render(request, 'notes/create_note.html', {'form': form, 'title': title})


@login_required
def create_notebook(request):
    form = NotebookForm()

    if request.method == 'POST':
        form = NotebookForm(request.POST)

        if form.is_valid():
            notebook = form.save(commit=False)
            notebook.user = request.user
            notebook.save()

            return redirect('notes:index')

    return render(request, 'notes/create_notebook.html', {'form': form})


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('notes:index')
    
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            user.email = request.POST['email']
            user.save()

            login(request, user)

            return redirect('notes:index')
    
    return render(request, 'notes/sign-up.html', {'form': form})
