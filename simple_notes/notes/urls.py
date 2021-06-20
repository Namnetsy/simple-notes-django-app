from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import *

app_name = 'notes'

urlpatterns = [
    path('', index, name='index'),
    path('log-in/', LoginView.as_view(template_name='notes/log-in.html', redirect_authenticated_user=True), name='log-in'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('log-out/', LogoutView.as_view(), name='log-out'),
    path('notebooks/create/', create_notebook, name='create-notebook'),
    path('notebooks/<str:notebook_title>/view/', view_notes, name='view-notes'),
    path('notebooks/<str:notebook_title>/edit/', edit_notebook, name='edit-notebook'),
    path('notebooks/<str:notebook_title>/remove/', remove_notebook, name='remove-notebook'),
    path('notebooks/<str:notebook_title>/notes/<str:note_title>/edit/', edit_note, name='edit-note'),
    path('notebooks/<str:notebook_title>/notes/<str:note_title>/remove/', remove_note, name='remove-note'),
    path('notebooks/<str:notebook_title>/notes/<str:note_title>/share/', share_note, name='share-note'),
    path('notebooks/<str:title>/notes/create/', create_note, name='create-note'),
    path('shared-notes/<str:unique_secret>/remove/', remove_shared_note, name='remove-shared-note'),
    path('shared-notes/<str:unique_secret>/view/', view_shared_note, name='view-shared-note'),
    path('settings/', settings, name='settings'),
    path('notebooks/<str:notebook_title>/notes/<str:note_title>/export-to-pdf/', export_to_pdf, name='export-to-pdf'),
    path('activate-account/<str:token>', activate_account, name='activate-account'),
    path('reminders/<str:notebook_title>/notes/<str:note_title>/remind-me', set_reminder, name='set-reminder'),
    path('reminders/<str:notebook_title>/notes/<str:note_title>/cancel', remove_reminder, name='remove-reminder'),
    path('versions/<str:notebook_title>/notes/<str:note_title>/list', view_note_versions, name='view-note-versions'),
    path('versions/<str:notebook_title>/notes/<str:note_title>/add', add_note_version, name='add-note-version'),
    path('versions/<str:notebook_title>/notes/<int:note_id>/restore', restore_note_version, name='restore-note-version'),
    path('versions/<str:notebook_title>/notes/<int:note_id>/view', view_note_version, name='view-note-version'),
    path('versions/<str:notebook_title>/notes/<int:note_id>/remove', remove_note_version, name='remove-note-version'),
]
