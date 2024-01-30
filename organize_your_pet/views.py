from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic import UpdateView

from organize_your_pet.forms import AddPetForm, PetSearchForm
from organize_your_pet.models import Visit, Pet


# from organize_your_pet.models import


class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'home_page/base.html')


class AboutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'home_page/about.html')


class DashboardView(View):

    def get(self, request):
        closest_visit = Visit.objects.filter(pet__owner=request.user).order_by('available_date__date').first()
        ctx = {
            'closest_visit': closest_visit
        }
        return render(request, 'accounts/dashboard.html', ctx)


class AddPetView(LoginRequiredMixin, View):
    def get(self, request):
        form = AddPetForm()
        ctx = {'form': form}
        return render(request, 'OYP/add_form_for_logged_in.html', ctx)

    def post(self, request):
        form = AddPetForm(request.POST)
        ctx = {'form': form}
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = self.request.user
            pet.save()
            return redirect('pets_list')
        return render(request, 'OYP/add_form_for_logged_in.html', ctx)


class PetsListView(LoginRequiredMixin, View):
    def get(self, request):
        pets = Pet.objects.filter(owner=request.user)
        form = PetSearchForm()
        if form.is_valid():
            name = form.cleaned_data.get('name', '')
            pets = pets.filter(name__icontains=name)
        ctx = {'form': form, 'list_elements': pets}
        return render(request, 'OYP/list_elements.html', ctx)


class PetDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        return HttpResponse('szczegóły zwierzaka')


class ModifyPetView(UserPassesTestMixin, View):
    def get(self, request, pk):
        return HttpResponse('edytuj zwierzaka')


class DeletePetView(LoginRequiredMixin, View):
    def get(self, request, pk):
        return HttpResponse('usuń zwierzaka')


class BookAppointmentView(LoginRequiredMixin, View):
    def get(self, request):
        return HttpResponse('zabookuj wizytę u weta')


class VisitsListView(LoginRequiredMixin, View):
    def get(self, request):
        return HttpResponse('lista wizyt')


class VisitDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        return HttpResponse('info o wizycie')


class VisitModifyView(UserPassesTestMixin, View):
    def get(self, request, pk):
        return HttpResponse('edytowanie info o konkretnej wizycie')


class DeleteVisitView(LoginRequiredMixin, View):
    def get(self, request, pk):
        return HttpResponse('usuń wizytę')
