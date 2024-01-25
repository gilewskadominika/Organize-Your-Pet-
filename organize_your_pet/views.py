from datetime import datetime
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


class AddPetView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponse('dodaj zwierzaka')
        return redirect('login_view')


class ListPetView(View):
    def get(self, request):
        return HttpResponse('lista zwierzaków')


class ModifyPetView(View):
    def get(self, request):
        return HttpResponse('edytuj zwierzaka')


class DashboardView(View):
    def get(self, request):
        return render(request, 'dashboard.html')


class BookAppointmentView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponse('zabookuj wizytę u weta')
        return redirect('login_view')


class VisitsListView(View):
    def get(self, request):
        return HttpResponse('Lista wizyt')


class VisitInfoView(View):
    def get(self, request, id):
        return HttpResponse('info o konkretnej wizycie')


class VisitModifyView(View):
    def get(self, request, id):
        return HttpResponse('edytowanie info o konkretnej wizycie')
