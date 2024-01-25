from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from accounts.forms import RegistrationForm, LoginForm


class RegistrationView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = RegistrationForm()
        ctx = {'form': form}
        return render(request, 'add_form.html', ctx)

    def post(self, request):
        form = RegistrationForm(request.POST)
        ctx = {'form': form}
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            login(request, user)
            return redirect('index')
        return render(request, 'add_form.html', ctx)


class LoginView(View):

    def get(self, request):
        # if request.user.is_authenticated:
        #     return redirect('dashboard')
        form = LoginForm()
        ctx = {'form': form}
        return render(request, 'add_form.html', ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        ctx = {'form': form}
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next = request.GET.get('next', 'dashboard')
                return redirect(next)
        return render(request, 'add_form.html', ctx)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


class ProfileView(View):
    def get(self, request):
        return HttpResponse('Wyświetla profil')