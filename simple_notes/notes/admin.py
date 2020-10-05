from django.contrib import admin
from .models import Notebook, Note, PublicSharedNote

admin.site.register(
    [Notebook, Note, PublicSharedNote]
)
