from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import auth_login
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views import View
from django.contrib import messages
from django.db import IntegrityError

from .forms import NotebookForm, NoteForm, UserSettingsForm
from .models import Notebook, Note, PublicSharedNote


def index(request):
    if request.user.is_authenticated:
        notebooks = Notebook.objects.filter(user=request.user)

        return render(request, 'notes/home.html', {'notebooks': notebooks})
    
    return render(request, 'notes/index.html')


@login_required
def share_note(request, notebook_title, note_title):
    notebook = get_object_or_404(Notebook, user=request.user, title=notebook_title)
    note = get_object_or_404(Note, notebook=notebook, title=note_title)

    try:
        sharedNote = PublicSharedNote.objects.create(user=request.user, note=note)

        messages.success(request, f'Public link for {note_title} was created successfully.')
    except IntegrityError:
        messages.warning(request, f'You have shared this note already!')
    
    return redirect('notes:view-shared-notes')


@login_required
def view_shared_notes(request):
    shared_notes = PublicSharedNote.objects.filter(user=request.user)

    return render(request, 'notes/view-shared-notes.html', {'shared_notes': shared_notes})


@login_required
def remove_note(request, notebook_title, note_title):
    notebook = get_object_or_404(Notebook, user=request.user, title=notebook_title)
    get_object_or_404(Note, notebook=notebook, title=note_title).delete()

    messages.success(request, f'{note_title} was removed successfully.')

    return redirect(reverse('notes:view-notes', args=[notebook_title]))


@login_required
def edit_notebook(request, notebook_title):
    notebook = get_object_or_404(Notebook, user=request.user, title=notebook_title)
    form = NotebookForm(instance=notebook)

    if request.method == 'POST':
        form = NotebookForm(request.POST, instance=notebook)

        if form.is_valid():
            notebook = form.save(commit=False)
            notebook.user = request.user
            notebook.save()

            messages.success(request, f'Changes in {notebook_title} were saved successfully.')

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

            messages.success(request, f'Your settings were saved successfully.')

            return redirect('notes:index')

    return render(request, 'notes/settings.html', {'form': form})


@login_required
def remove_notebook(request, notebook_title):
    get_object_or_404(Notebook, user=request.user, title=notebook_title).delete()

    messages.success(request, f'{notebook_title} was removed successfully.')

    return redirect('notes:index')


@login_required
def view_notes(request, notebook_title):
    notebook = get_object_or_404(Notebook, user=request.user, title=notebook_title)
    notes = Note.objects.filter(notebook=notebook)

    context = {
        'notes': notes,
        'notebook_title': notebook_title,
    }

    return render(request, 'notes/view-notes.html', context)


@login_required
def remove_all_shared_notes(request):
    shared_notes = PublicSharedNote.objects.filter(user=request.user)

    if shared_notes.exists():
        shared_notes.delete()
        messages.success(request, 'All shared notes were removed sucessfully.')
    else:
        messages.warning(request, 'You have zero shared notes, so there\'s nothing to remove!')

    return redirect('notes:view-shared-notes')


@login_required
def remove_shared_note(request, unique_secret):
    get_object_or_404(PublicSharedNote, unique_secret=unique_secret).delete()

    messages.success(request, 'Shared note was removed sucessfully.')

    return redirect('notes:view-shared-notes')


def view_shared_note(request, unique_secret):
    shared_note = get_object_or_404(PublicSharedNote, unique_secret=unique_secret)

    return render(request, 'notes/view-shared-note.html', {'shared_note': shared_note})


@login_required
def edit_note(request, notebook_title, note_title):
    notebook = get_object_or_404(Notebook, user=request.user, title=notebook_title)
    note = get_object_or_404(Note, notebook=notebook, title=note_title)
    form = NoteForm(instance=note)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)

        if form.is_valid():
            note = form.save(commit=False)
            note.modified_at = timezone.now()
            note.save()

            messages.success(request, f'Changes in {note_title} were saved successfully.')
            return redirect(reverse('notes:view-notes', args=[notebook_title]))
    
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
            notebook = get_object_or_404(Notebook, user=request.user, title=title)
            note = form.save(commit=False)
            note.notebook = notebook
            note.save()

            messages.success(request, f'{note.title} was created successfully.')

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

            messages.success(request, f'{notebook.title} was created successfully.')
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
