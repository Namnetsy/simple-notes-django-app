from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from . import model_defaults
from .utils import generate_token


User = get_user_model()


class BaseModel(models.Model):
    def __str__(self) -> str:
        return f"{self.__class__.__name__} ({self.pk})"

    def __repr__(self) -> str:
        return self.__str__()

    class Meta:
        abstract = True


class Notebook(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)

    def __str__(self) -> str:
        return f"{self.user.username}: {self.title}"

    class Meta:
        unique_together = ("user", "title")


class Note(BaseModel):
    notebook = models.ForeignKey(Notebook, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.notebook.user.username}: {self.title}"

    class Meta:
        unique_together = ("notebook", "title")


class NoteVersion(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    message = models.CharField(max_length=150, blank=True)
    title = models.CharField(max_length=150)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.user.username}[{self.created_at}]: {self.title}"


class PublicSharedNote(BaseModel):
    unique_secret = models.CharField(primary_key=True, max_length=43, default=generate_token)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user.username}: {self.note.title}"

    class Meta:
        unique_together = ("user", "note")


class Profile(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.CharField(
        max_length=20, choices=model_defaults.Language.choices, default=model_defaults.Language.EN
    )
    theme = models.CharField(max_length=20, choices=model_defaults.Theme.choices, default=model_defaults.Theme.DEFAULT)
    is_activated = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"[{self.language}]: {self.user.username}"


class ActivationToken(BaseModel):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    token = models.CharField(max_length=32, default=generate_token, unique=True)

    def __str__(self) -> str:
        return self.profile.user.username


class Reminder(BaseModel):
    task_id = models.CharField(max_length=36, primary_key=True)
    note = models.OneToOneField(Note, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.note.notebook.user}: {self.note.title}"
