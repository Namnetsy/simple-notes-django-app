from django import forms
from django.urls import reverse
from django.utils.translation import gettext as _, get_language

from .models import Notebook, Note, Profile, ActivationToken
from django.contrib.auth.models import User

from .utils import send_email


class NotebookForm(forms.ModelForm):
    class Meta:
        model = Notebook
        fields = ['title']


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['language', 'theme']


class UserAccountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)

        super().__init__(*args, **kwargs)

    password2 = forms.CharField(max_length=200, required=True)  # TODO: validate this field

    def save(self, commit=True):
        user = super(forms.ModelForm, self).save(commit=False)
        user.save()
        self.save_m2m()

        profile = Profile(user=user, language=get_language())
        profile.save()
        activation_token = ActivationToken(profile=profile)
        activation_token.save()

        activation_url = self.request.build_absolute_uri(
            reverse('notes:activate-account', args=[activation_token.token])
        )

        send_email(
            email=user.email,
            subject=_('Welcome to Simple Notes!'),
            content='''
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
            '''.format(
                greeting=_('Hey {username}!').format(username=user.username),
                thank_you=_('Thank you for signing up, just one more step... click on the link below in order to activate your account.'),
                activation_url=activation_url,
                activate_account=_('Activate Account'),
                notice=_("Without an activated account you won't be able to use features like reminders or password reset."),
            )
        )

        return user

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
