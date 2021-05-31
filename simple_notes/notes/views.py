from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils import timezone, translation
from django.utils.translation import gettext as _, get_language
from django.views import View
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse

from .forms import NotebookForm, NoteForm, UserSettingsForm, ProfileSettingsForm
from .models import Notebook, Note, PublicSharedNote, Profile
from xhtml2pdf import pisa
from tempfile import TemporaryFile


def index(request):
    if request.user.is_authenticated:
        user_settings_form = UserSettingsForm(instance=request.user)
        profile_settings_form = ProfileSettingsForm(instance=Profile.objects.get(user=request.user))
        ctx = general_context(request)
        ctx.update({
            'user_settings_form': user_settings_form,
            'profile_settings_form': profile_settings_form,
        })

        return render(request, 'notes/home.html', ctx)

    return render(request, 'notes/index.html')


@login_required
def share_note(request, notebook_title, note_title):
    notebook = get_object_or_404(Notebook, user=request.user, title=notebook_title)
    note = get_object_or_404(Note, notebook=notebook, title=note_title)

    try:
        PublicSharedNote.objects.create(user=request.user, note=note)

        messages.success(request, _('Public link for {note_title} was created successfully.').format(
            note_title=note_title
        ))
    except IntegrityError:
        messages.warning(request, _(f'You have shared this note already!'))

    return redirect(reverse('notes:view-notes', args=[notebook_title]))


@login_required
def remove_notebook(request, notebook_title):
    get_object_or_404(Notebook, user=request.user, title=notebook_title).delete()

    messages.success(request, _('{notebook_title} was removed successfully.').format(
        notebook_title=notebook_title
    ))

    return redirect('notes:index')


@login_required
def remove_note(request, notebook_title, note_title):
    notebook = get_object_or_404(Notebook, user=request.user, title=notebook_title)
    get_object_or_404(Note, notebook=notebook, title=note_title).delete()

    messages.success(request, _('{note_title} was removed successfully.').format(note_title=note_title))

    return redirect(reverse('notes:view-notes', args=[notebook_title]))


@login_required
def remove_shared_note(request, unique_secret):
    get_object_or_404(PublicSharedNote, unique_secret=unique_secret).delete()

    messages.success(request, _('Shared note was removed successfully.'))

    return redirect('notes:view-shared-notes')


@login_required
def edit_notebook(request, notebook_title):
    if request.method == 'POST':
        form = NotebookForm(request.POST)

        if form.is_valid():
            notebook = Notebook.objects.get(title=notebook_title)
            notebook.title = form.data['title']
            notebook.save()

            msg = _('Changes in {notebook_title} were saved successfully.').format(
                notebook_title=notebook_title
            )
            messages.success(request, msg)
        else:
            messages.error(request, _('Check your input!'))

    return redirect('notes:index')


@login_required
def edit_note(request, notebook_title, note_title):
    notebook = get_object_or_404(Notebook, user=request.user, title=notebook_title)
    note = get_object_or_404(Note, notebook=notebook, title=note_title)
    form = NoteForm(instance=note)

    if request.method == 'POST':
        # we need this crutch because there are two input fields for mobile and desktop
        titles = request.POST.getlist('title')
        new_title = titles[0] if titles[0] != note.title else titles[1]
        request.POST._mutable = True
        request.POST['title'] = new_title

        form = NoteForm(request.POST, instance=note)

        if form.is_valid():
            note.title = form.data.getlist('title')[0]
            note.content = form.data.getlist('content')[0]
            note.modified_at = timezone.now()
            note.save()

            messages.success(request, _('Changes in {note_title} were saved successfully.').format(
                note_title=note_title
            ))
        else:
            messages.error(request, _('The title field should NOT be empty!'))

    ctx = general_context(request, {
        'form': form,
        'notebook_title': notebook.title,
        'note_title': note.title,
    })

    return render(request, 'notes/edit-note.html', ctx)


@login_required
def settings(request):
    profile = Profile.objects.get(user=request.user)
    user_settings_form = UserSettingsForm(instance=request.user)
    profile_settings_form = ProfileSettingsForm(instance=profile)

    if request.method == 'POST':
        user_settings_form = UserSettingsForm({
            'username': request.POST.get('username'),
            'email': request.POST.get('email')
        }, instance=request.user)
        profile_settings_form = ProfileSettingsForm({
            'language': request.POST.get('language'),
            'theme': request.POST.get('theme'),
        }, instance=profile)

        if user_settings_form.is_valid() and profile_settings_form.is_valid():
            user_settings_form.save()
            profile_settings_form.save()

            translation.activate(profile_settings_form.cleaned_data['language'])

            messages.success(request, _('Your settings were saved successfully.'))

            return redirect('notes:index')

    return redirect('notes:index', {
        'user_settings_form': user_settings_form,
        'profile_settings_form': profile_settings_form,
    })


@login_required
def view_notes(request, notebook_title):
    notebook = get_object_or_404(Notebook, user=request.user, title=notebook_title)
    notes = Note.objects.filter(notebook=notebook)

    ctx = general_context(request, {
        'notes': notes,
        'notebook_title': notebook_title,
    })

    return render(request, 'notes/view-notes.html', ctx)


def view_shared_note(request, unique_secret):
    shared_note = get_object_or_404(PublicSharedNote, unique_secret=unique_secret)
    ctx = {
        'shared_note': shared_note,
    }
    ctx = general_context(request, ctx) if request.user.is_authenticated else ctx

    return render(request, 'notes/view-shared-note.html', ctx)


@login_required
def create_note(request, title):
    form = NoteForm(initial={'title': '', 'content': ''})

    if request.method == 'POST':
        # we need this crutch because there are two input fields for mobile and desktop
        titles = request.POST.getlist('title')
        new_title = titles[0] if titles[0] else titles[1]
        request.POST._mutable = True
        request.POST['title'] = new_title
        form = NoteForm(request.POST)

        if form.is_valid():
            notebook = get_object_or_404(Notebook, user=request.user, title=title)
            note = form.save(commit=False)
            note.notebook = notebook
            note.save()

            messages.success(request, _('{note_title} was created successfully.').format(note_title=note.title))

            return redirect(reverse('notes:edit-note', args=[notebook.title, note.title]))
        else:
            messages.error(request, _('The title field should NOT be empty!'))

    ctx = general_context(request, {
        'form': form,
        'notebook_title': title,
    })

    return render(request, 'notes/create_note.html', ctx)


@login_required
def create_notebook(request):
    if request.method == 'POST':
        form = NotebookForm(request.POST)

        if form.is_valid():
            notebook = form.save(commit=False)
            notebook.user = request.user
            notebook.save()

            messages.success(request, _('{notebook_title} was created successfully.').format(
                notebook_title=notebook.title
            ))

            return redirect(reverse('notes:view-notes', args=[notebook.title]))
        else:
            messages.error(request, form.errors['title'])

    return redirect('notes:index')


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

            Profile(user=user, language=get_language()).save()

            login(request, user)

            return redirect('notes:index')

        return render(request, 'notes/sign-up.html', {'form': form})


def general_context(request, context=None):
    notebooks = Notebook.objects.filter(user=request.user)
    shared_notes = PublicSharedNote.objects.filter(user=request.user)
    theme = Profile.objects.get(user=request.user).theme
    data = {
        'notebooks': notebooks,
        'shared_notes': shared_notes,
        'theme': theme
    }

    for notebook in data['notebooks']:
        notebook.notes_count = Note.objects.filter(
            notebook=notebook
        ).count()

    if context:
        if 'notes' not in context and 'notebook_title' in context:
            notebook = Notebook.objects.get(user=request.user, title=context['notebook_title'])
            context.update({'notes': Note.objects.filter(notebook=notebook)})

        context.update(data)

        return context

    return data


@login_required
def export_to_pdf(request, notebook_title, note_title):
    notebook = Notebook.objects.get(user=request.user, title=notebook_title)
    note = Note.objects.get(notebook=notebook, title=note_title)

    tmpFile = TemporaryFile(mode='w+b')
    pisa.CreatePDF(note.content, tmpFile)
    tmpFile.seek(0)
    pdf = tmpFile.read()
    content_disposition = f'attachment; filename="{note_title}.pdf"'

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = content_disposition

    tmpFile.close()

    return response
