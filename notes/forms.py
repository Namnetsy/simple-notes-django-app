from django import forms
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import get_language
from django.utils.translation import gettext as _

from .models import ActivationToken, Note, Notebook, NoteVersion, Profile
from .tasks import send_email_task


User = get_user_model()


class NotebookForm(forms.ModelForm):
    class Meta:
        model = Notebook
        fields = ("title",)


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ("title", "content")


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email")


class ProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("language", "theme")


class UserAccountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)

        super().__init__(*args, **kwargs)

    def save(self, commit: bool = True) -> User:
        user = super(forms.ModelForm, self).save(commit=False)
        user.set_password(user.password)
        user.save()
        self.save_m2m()

        profile = Profile(user=user, language=get_language())
        profile.save()
        activation_token = ActivationToken(profile=profile)
        activation_token.save()

        activation_url = self.request.build_absolute_uri(
            reverse("notes:activate-account", args=[activation_token.token])
        )

        send_email_task.delay(
            email=user.email,
            subject=_("Welcome to Simple Notes!"),
            content="""
                <html>
                    <body>
                        <p>{greeting}</p>
                        <p>{thank_you}</p>
                        <p>
                            <a href="{activation_url}">{activate_account}</a>
                        </p>
                        <small>{notice}</small>
                    </body>
                </html>
            """.format(
                greeting=_("Hey {username}!").format(username=user.username),
                thank_you=_(
                    "Thank you for signing up, just one more step... "
                    "click on the link below in order to activate your account."
                ),
                activation_url=activation_url,
                activate_account=_("Activate Account"),
                notice=_(
                    "Without an activated account you won't be able to use features like reminders or password reset."
                ),
            ),
        )

        return user

    class Meta:
        model = User
        fields = ("username", "password", "email")


class AddNoteVersionForm(forms.ModelForm):
    message = forms.CharField(max_length=150, required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        self.note = kwargs.pop("note", None)

        super().__init__(*args, **kwargs)

    def save(self, commit: bool = True) -> NoteVersion:
        note_version = super(forms.ModelForm, self).save(commit=False)
        note_version.user = self.request.user
        note_version.note = self.note
        note_version.title = self.note.title
        note_version.content = self.note.content
        note_version.save()

        return note_version

    class Meta:
        model = NoteVersion
        fields = ("message",)
