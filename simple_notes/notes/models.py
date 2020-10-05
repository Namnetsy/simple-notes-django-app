from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from secrets import token_urlsafe

class Notebook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.user.username}: {self.title}'
    

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


def generate_token():
    return token_urlsafe(32)


class PublicSharedNote(models.Model):
    unique_secret = models.CharField(primary_key=True, max_length=43, default=generate_token)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}: {self.note.title}'
