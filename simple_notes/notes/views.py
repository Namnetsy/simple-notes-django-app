from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import auth_login
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views import View

from .forms import NotebookForm, NoteForm, UserSettingsForm
from .models import Notebook, Note, PublicSharedNote


def index(request):
    if request.user.is_authenticated:
        notebooks = Notebook.objects.filter(user=request.user)

        return render(request, 'notes/home.html', {'notebooks': notebooks})
    
    return render(request, 'notes/index.html')


@login_required
def share_note(request, notebook_title, note_title):
    notebook = Notebook.objects.get(user=request.user, title=notebook_title)
    note = Note.objects.get(notebook=notebook, title=note_title)

    sharedNote = PublicSharedNote.objects.create(user=request.user, note=note)
    
    return redirect('notes:view-shared-notes')


@login_required
def view_shared_notes(request):
    shared_notes = PublicSharedNote.objects.filter(user=request.user)

    return render(request, 'notes/view-shared-notes.html', {'notes': shared_notes})


@login_required
def remove_note(request, notebook_title, note_title):
    notebook = Notebook.objects.get(user=request.user, title=notebook_title)
    Note.objects.get(notebook=notebook, title=note_title).delete()

    return redirect(reverse('notes:view-notes', args=[notebook_title]))


@login_required
def remove_notebook(request, notebook_title):
    Notebook.objects.get(user=request.user, title=notebook_title).delete()

    return redirect('notes:index')


@login_required
def edit_notebook(request, notebook_title):
    notebook = Notebook.objects.get(user=request.user, title=notebook_title)
    form = NotebookForm(instance=notebook)

    if request.method == 'POST':
        form = NotebookForm(request.POST, instance=notebook)

        if form.is_valid():
            notebook = form.save(commit=False)
            notebook.user = request.user
            notebook.save()

            return redirect('notes:index')

    context = {
        'form': form,
        'notebook_title': notebook_title,
    }

    return render(request, 'notes/edit-notebook.html', context)


@login_required
def settings(request):
    form = UserSettingsForm(instance=request.user)

    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()

            return redirect('notes:index')

    return render(request, 'notes/settings.html', {'form': form})


@login_required
def remove_notebook(request, notebook_title):
    Notebook.objects.get(user=request.user, title=notebook_title).delete()

    return redirect('notes:index')


@login_required
def view_notes(request, notebook_title):
    notebook = Notebook.objects.get(user=request.user, title=notebook_title)
    notes = Note.objects.filter(notebook=notebook)

    context = {
        'notes': notes,
        'notebook_title': notebook_title,
    }

    return render(request, 'notes/view-notes.html', context)


def view_shared_note(request, secret):
    pass


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


class SignUp(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('notes:index')
        
        form = UserCreationForm()

        return render(request, 'notes/sign-up.html', {'form': form})
    
    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.email = request.POST['email']
            user.save()
            form.save_m2m()

            login(request, user)

            return redirect('notes:index')
        
        return render(request, 'notes/sign-up.html', {'form': form})
