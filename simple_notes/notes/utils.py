import json

from django.urls import reverse

from notes.models import Note, Notebook


def serialize_notebooks_with_notes(request):
    result = []
    for notebook in Notebook.objects.filter(user=request.user):
        result.append({
            'notebook_title': notebook.title,
            'notebook_url': request.build_absolute_uri(reverse('notes:view-notes', args=[notebook.title])),
        })

        for note in Note.objects.filter(notebook=notebook):
            result.append({
                'notebook_title': notebook.title,
                'note_title': note.title,
                'note_url': request.build_absolute_uri(reverse('notes:edit-note', args=[notebook.title, note.title])),
            })

    return json.dumps(result)
