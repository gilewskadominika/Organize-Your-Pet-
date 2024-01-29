from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
# from organize_your_pet.models import


class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'base.html')


class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')


class AddPetView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponse('dodaj zwierzaka')
        return redirect('login_view')


class PetsListView(LoginRequiredMixin, View):
    def get(self, request):
        return HttpResponse('lista zwierzaków')

# generyczny, z functest userpassestestmixin, updateview
class ModifyPetView(View):
    def get(self, request):
        return HttpResponse('edytuj zwierzaka')


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'dashboard.html')


class BookAppointmentView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponse('zabookuj wizytę u weta')
        return redirect('login_view')


class VisitsListView(LoginRequiredMixin, View):
    def get(self, request):
        return HttpResponse('Lista wizyt')


class VisitInfoView(LoginRequiredMixin, View):
    def get(self, request, id):
        return HttpResponse('info o konkretnej wizycie')

# generyczny, z functest userpassestestmixin, updateview
class VisitModifyView(View):
    def get(self, request, id):
        return HttpResponse('edytowanie info o konkretnej wizycie')
