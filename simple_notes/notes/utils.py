import json

from django.conf import settings
from django.urls import reverse

from notes.models import Note, Notebook

from pepipost.pepipost_client import PepipostClient
from pepipost.models.send import Send
from pepipost.models.mfrom import From
from pepipost.models.content import Content
from pepipost.models.type_enum import TypeEnum
from pepipost.models.personalizations import Personalizations
from pepipost.models.email_struct import EmailStruct
from pepipost.exceptions.api_exception import APIException

from secrets import token_urlsafe


def serialize_notebooks_with_notes(request: object) -> str:
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


def send_email(subject: str, email: str, content: str) -> bool:
    api_key = settings.PEPIPOST_API_KEY
    client = PepipostClient(api_key)

    mail_send_controller = client.mail_send
    body = Send()
    body.mfrom = From(email=settings.PEPIPOST_FROM_EMAIL, name=settings.PEPIPOST_FROM_NAME)
    body.subject = subject
    body.content = [Content(
        mtype=TypeEnum.HTML,
        value=content
    )]
    body.personalizations = [Personalizations(to=[EmailStruct(email=email)])]

    try:
        return json.loads(mail_send_controller.create_generatethemailsendrequest(body)).get('message') == 'OK'
    except APIException as e:
        print(e)

    return False


def generate_token(length=32) -> str:
    """Return url safe randomly generated token."""

    return token_urlsafe(length)
