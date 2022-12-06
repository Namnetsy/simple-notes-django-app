from django.contrib import admin

from . import models


admin.site.register(
    [
        models.Notebook,
        models.Note,
        models.PublicSharedNote,
        models.NoteVersion,
        models.ActivationToken,
        models.Reminder,
        models.Profile,
    ]
)
