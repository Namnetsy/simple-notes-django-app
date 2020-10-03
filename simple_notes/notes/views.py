from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import auth_login
from django.contrib.auth import login, logout


def index(request):
    return render(request, 'notes/index.html')


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('notes:index')
    
    form = None

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        print(form.is_valid())

        if form.is_valid():
            user = form.save()
            print(user)

            user.email = request.POST['email']
            user.save()

            login(request, user)

            return redirect('notes:index')
    
    return render(request, 'notes/sign-up.html', {'form': form})
