from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.utils import timezone

from .utils import generate_token


class Notebook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.user.username}: {self.title}'
    
    class Meta:
        unique_together = ('user', 'title')


class Note(models.Model):
    notebook = models.ForeignKey(Notebook, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.notebook.user.username}: {self.title}'
    
    class Meta:
        unique_together = ('notebook', 'title')


class PublicSharedNote(models.Model):
    unique_secret = models.CharField(primary_key=True, max_length=43, default=generate_token)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}: {self.note.title}'
    
    class Meta:
        unique_together = ('user', 'note')


class Theme:
    DEFAULT = 'default'
    LUX = 'lux'
    PULSE = 'pulse'
    SANDSTONE = 'sandstone'

    CHOICES = (
        (DEFAULT, _('Default')),
        (LUX, 'Lux'),
        (PULSE, 'Pulse'),
        (SANDSTONE, 'Sandstone')
    )


class Language:
    UK = 'uk'
    EN = 'en'

    CHOICES = (
        (UK, _('Ukrainian')),
        (EN, _('English'))
    )


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=20, choices=Language.CHOICES, default=Language.EN)
    theme = models.CharField(max_length=20, choices=Theme.CHOICES, default=Theme.DEFAULT)
    is_activated = models.BooleanField(default=False)

    def __str__(self):
        return f'[{self.language}]: {self.user.username}'


class ActivationToken(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, unique=True)
    token = models.CharField(max_length=32, default=generate_token, unique=True)

    def __str__(self):
        return self.profile.user.username
