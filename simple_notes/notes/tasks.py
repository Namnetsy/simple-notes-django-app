from celery import shared_task

from notes.utils import send_email

from django.utils.translation import gettext as _


@shared_task
def send_email_task(subject: str, email: str, content: str):
    print(f'SEND_EMAIL_TASK: Sending an email to {email}')

    if send_email(subject, email, content):
        print(f'SEND_EMAIL_TASK: Email was sent to {email}')
        return

    print(f'ERROR_DURING_SEND_EMAIL_TASK: Error')
