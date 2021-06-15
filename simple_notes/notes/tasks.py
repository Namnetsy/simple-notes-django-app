from celery import shared_task

from .utils import send_email

from django.utils.translation import gettext as _

from .models import Reminder


@shared_task
def send_email_task(subject: str, email: str, content: str):
    print(f'SEND_EMAIL_TASK: Sending an email to {email}')

    if send_email(subject, email, content):
        print(f'SEND_EMAIL_TASK: Email was sent to {email}')
        return

    print(f'ERROR_DURING_SEND_EMAIL_TASK: Error')


@shared_task
def send_reminder_task(
    username: str,
    email: str,
    notebook_title: str,
    note_name: str,
    note_full_link: str
):
    print(f'SEND_REMINDER_TASK: Sending a reminder for {username}')

    send_email(
        email=email,
        subject=_('Don\'t forget about {note_name} | Simple Notes Reminder').format(note_name=note_name),
        content='''
                <html>
                    <body>
                        <p>{greeting}</p>
                        <p>{text}</p>
                        <p>
                            <a href="{note_full_url}">{go_to_note}</a>
                        </p>
                    </body>
                </html>
            '''.format(
            greeting=_('Hey {username}!').format(username=username),
            text=_('You wanted to be reminded about {note_name}. Click on the link below in order to open it.')
                .format(note_name=note_name),
            note_full_url=note_full_link,
            go_to_note=_('Open {note_name}').format(note_name=note_name),
        )
    )

    Reminder.objects.get(
        note__notebook__user__username=username,
        note__notebook__title=notebook_title,
        note__title=note_name,
    ).delete()

    print(f'SEND_REMINDER_TASK: Reminder for {username} was sent')
