import json
from secrets import token_urlsafe
from typing import List

from django.conf import settings
from django.db.models import F
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import get_language
from pepipost.exceptions.api_exception import APIException
from pepipost.models.content import Content
from pepipost.models.email_struct import EmailStruct
from pepipost.models.mfrom import From
from pepipost.models.personalizations import Personalizations
from pepipost.models.send import Send
from pepipost.models.type_enum import TypeEnum
from pepipost.pepipost_client import PepipostClient


def serialize_notebooks_with_notes(request) -> str:
    from .models import Note, Notebook

    notes = (
        Note.objects.filter(notebook__user=request.user)
        .only("notebook__title", "title")
        .values("notebook__title", "title")
    )

    notebooks = Notebook.objects.filter(user=request.user).only("id", "title").values("id", "title")

    notebook_ids: List[int] = []
    result = []
    for notebook in notebooks:
        title = notebook["title"]
        notebook_ids.append(notebook["id"])

        result.append(
            {
                "notebook_title": title,
                "notebook_url": request.build_absolute_uri(reverse("notes:view-notes", args=[title])),
            }
        )

    notes = (
        Note.objects.filter(notebook__in=notebook_ids)
        .only("notebook__title", "title")
        .annotate(notebook_title=F("notebook__title"))
        .values("notebook_title", "title")
    )

    if not notes:
        return json.dumps(result)

    for note in notes:
        title, notebook_title = note["title"], note["notebook_title"]

        result.append(
            {
                "notebook_title": notebook_title,
                "note_title": title,
                "note_url": request.build_absolute_uri(reverse("notes:edit-note", args=[notebook_title, title])),
            }
        )

    return json.dumps(result)


def send_email(subject: str, email: str, content: str) -> bool:
    api_key = settings.PEPIPOST_API_KEY
    client = PepipostClient(api_key)

    mail_send_controller = client.mail_send
    body = Send()
    body.mfrom = From(email=settings.PEPIPOST_FROM_EMAIL, name=settings.PEPIPOST_FROM_NAME)
    body.subject = subject
    body.content = [Content(mtype=TypeEnum.HTML, value=content)]
    body.personalizations = [Personalizations(to=[EmailStruct(email=email)])]

    try:
        return json.loads(mail_send_controller.create_generatethemailsendrequest(body)).get("message") == "OK"
    except APIException as e:
        print(e)

    return False


def generate_token(length: int = 32) -> str:
    """Return url safe randomly generated token."""

    return token_urlsafe(length)


def redirect_back(request):
    return redirect(
        request.META.get("HTTP_REFERER", "/")
        .replace("/uk/", f"/{get_language()}/")
        .replace("/en/", f"/{get_language()}/")
    )
