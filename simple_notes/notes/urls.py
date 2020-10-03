from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import index, sign_up

app_name = 'notes'

urlpatterns = [
    path('', index, name='index'),
    path('log-in/', LoginView.as_view(template_name='notes/log-in.html', redirect_authenticated_user=True), name='log-in'),
    path('sign-up/', sign_up, name='sign-up'),
    path('log-out/', LogoutView.as_view(), name='log-out'),
]
