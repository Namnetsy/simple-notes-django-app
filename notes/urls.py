from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views


app_name = "notes"

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "log-in/", LoginView.as_view(template_name="notes/log-in.html", redirect_authenticated_user=True), name="log-in"
    ),
    path("sign-up/", views.SignUp.as_view(), name="sign-up"),
    path("log-out/", LogoutView.as_view(), name="log-out"),
    path("notebooks/create/", views.create_notebook, name="create-notebook"),
    path("notebooks/<str:notebook_title>/view/", views.view_notes, name="view-notes"),
    path("notebooks/<str:notebook_title>/edit/", views.edit_notebook, name="edit-notebook"),
    path("notebooks/<str:notebook_title>/remove/", views.remove_notebook, name="remove-notebook"),
    path("notebooks/<str:notebook_title>/notes/<str:note_title>/edit/", views.edit_note, name="edit-note"),
    path("notebooks/<str:notebook_title>/notes/<str:note_title>/remove/", views.remove_note, name="remove-note"),
    path("notebooks/<str:notebook_title>/notes/<str:note_title>/share/", views.share_note, name="share-note"),
    path("notebooks/<str:title>/notes/create/", views.create_note, name="create-note"),
    path("shared-notes/<str:unique_secret>/remove/", views.remove_shared_note, name="remove-shared-note"),
    path("shared-notes/<str:unique_secret>/view/", views.view_shared_note, name="view-shared-note"),
    path("settings/", views.settings, name="settings"),
    path(
        "notebooks/<str:notebook_title>/notes/<str:note_title>/export-to-pdf/",
        views.export_to_pdf,
        name="export-to-pdf",
    ),
    path("activate-account/<str:token>", views.activate_account, name="activate-account"),
    path("reminders/<str:notebook_title>/notes/<str:note_title>/remind-me", views.set_reminder, name="set-reminder"),
    path("reminders/<str:notebook_title>/notes/<str:note_title>/cancel", views.remove_reminder, name="remove-reminder"),
    path(
        "versions/<str:notebook_title>/notes/<str:note_title>/list", views.view_note_versions, name="view-note-versions"
    ),
    path("versions/<str:notebook_title>/notes/<str:note_title>/add", views.add_note_version, name="add-note-version"),
    path(
        "versions/<str:notebook_title>/notes/<int:note_id>/restore",
        views.restore_note_version,
        name="restore-note-version",
    ),
    path("versions/<str:notebook_title>/notes/<int:note_id>/view", views.view_note_version, name="view-note-version"),
    path(
        "versions/<str:notebook_title>/notes/<int:note_id>/remove",
        views.remove_note_version,
        name="remove-note-version",
    ),
]
