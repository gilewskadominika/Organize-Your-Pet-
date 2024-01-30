from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic import UpdateView

from organize_your_pet.forms import AddPetForm
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
        closest_visit = Visit.objects.all().order_by('available_date__date').first()
        ctx = {
            'closest_visit': closest_visit
        }
        return render(request, 'accounts/dashboard.html', ctx)


class AddPetView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            form = AddPetForm()
            ctx = {'form': form}
            return render(request, 'OYP/add_pet_form.html', ctx)
        return redirect('login_view')

    def post(self, request):
        form = AddPetForm(request.POST)
        ctx = {'form': form}
        if form.is_valid():
            name = form.cleaned_data['name']
            species = form.cleaned_data['species']
            other_species = form.cleaned_data['other_species']
            breed = form.cleaned_data['breed']
            gender = form.cleaned_data['gender']
            birth_date = form.cleaned_data['birth_date']
            weight = form.cleaned_data['weight']
            chip = form.cleaned_data['chip']
            # pet.owner = self.request.user
            pet = Pet.objects.create(name=name, species=species, other_species=other_species,
                                     breed=breed, gender=gender, birth_date=birth_date,
                                     weight=weight, chip=chip)
            return redirect('pets_list')
        return render(request, 'OYP/add_pet_form.html', ctx)


class PetsListView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponse('lista zwierzaków')
        return redirect('login_view')


class ModifyPetView(LoginRequiredMixin, View):
    def get(self, request):
        return HttpResponse('edytuj zwierzaka')


class BookAppointmentView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponse('zabookuj wizytę u weta')
        return redirect('login_view')


class VisitsListView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponse('lista wizyt')
        return redirect('login_view')


class VisitInfoView(LoginRequiredMixin, View):
    def get(self, request, id):
        if request.user.is_authenticated:
            return HttpResponse('info o wizycie')
        return redirect('login_view')


class VisitModifyView(LoginRequiredMixin, View):
    def get(self, request, id):
        return HttpResponse('edytowanie info o konkretnej wizycie')
