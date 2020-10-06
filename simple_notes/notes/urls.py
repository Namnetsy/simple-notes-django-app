from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import index, sign_up, create_notebook, create_note, edit_note, view_notes

app_name = 'notes'

urlpatterns = [
    path('', index, name='index'),
    path('log-in/', LoginView.as_view(template_name='notes/log-in.html', redirect_authenticated_user=True), name='log-in'),
    path('sign-up/', sign_up, name='sign-up'),
    path('log-out/', LogoutView.as_view(), name='log-out'),
    path('create-notebook/', create_notebook, name='create-notebook'),
    path('notebooks/<str:title>/notes/', create_note, name='create-note'),
    path('notebooks/<str:notebook_title>/notes/<str:note_title>/', edit_note, name='edit-note'),
    path('notebooks/<str:notebook_title>', view_notes, name='view-notes'),
]
