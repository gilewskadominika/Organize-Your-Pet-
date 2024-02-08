from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import UpdateView

from accounts.forms import RegistrationForm, LoginForm


class RegistrationView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = RegistrationForm()
        ctx = {'form': form}
        return render(request, 'OYP/add_form_for_unlogged.html', ctx)

    def post(self, request):
        form = RegistrationForm(request.POST)
        ctx = {'form': form}
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            login(request, user)
            return redirect('dashboard')
        return render(request, 'OYP/add_form_for_unlogged.html', ctx)


class LoginView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = LoginForm()
        ctx = {'form': form}
        return render(request, 'OYP/add_form_for_unlogged.html', ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        ctx = {'form': form}
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if not user:
                ctx['error_message'] = 'Nieprawidłowe dane logowania'
            if user is not None:
                login(request, user)
                next = request.GET.get('next', 'dashboard')
                return redirect(next)
        return render(request, 'OYP/add_form_for_unlogged.html', ctx)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('index')


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        ctx = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email
        }
        return render(request, 'accounts/profile.html', ctx)


class ProfileEditView(UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'accounts/profile_edit.html'
    fields = ['email', 'username', 'first_name', 'last_name']

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile

    def get_success_url(self):
        return reverse('profile_view')
