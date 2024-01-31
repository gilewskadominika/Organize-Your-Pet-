from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.views import View
from django.views.generic import UpdateView

from organize_your_pet.forms import AddPetForm, PetSearchForm, AddVisitForm, VisitSearchForm
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
        form = PetSearchForm(request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name', '')
            pets = pets.filter(name__icontains=name)
        ctx = {'form': form, 'list_elements': pets}
        return render(request, 'OYP/pets_list_elements.html', ctx)


class PetDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        pet = Pet.objects.get(pk=pk)
        ctx = {'pet': pet}
        return render(request, 'OYP/pet_detail.html', ctx)


class ModifyPetView(LoginRequiredMixin, UpdateView):
    model = Pet
    template_name = 'OYP/add_form_for_logged_in.html'
    form_class = AddPetForm

    def get_success_url(self):
        return reverse('pet_info', args=(self.object.pk,))


class DeletePetView(LoginRequiredMixin, View):
    def get(self, request, pk):
        pet = Pet.objects.get(pk=pk)
        ctx = {'pet': pet}
        return render(request, 'OYP/pet_delete_conf.html', ctx)

    def post(self, request, pk):
        pet = Pet.objects.get(pk=pk)
        pet.delete()
        return redirect('pets_list')


class BookAppointmentView(LoginRequiredMixin, View):
    def get(self, request):
        return HttpResponse('zabookuj wizytę u weta')


class VisitsListView(LoginRequiredMixin, View):
    def get(self, request):
        visits = Visit.objects.filter(pet__owner=request.user)
        form = VisitSearchForm(request.GET)
        if form.is_valid():
            available_date__date = form.cleaned_data.get('available_date__date', '')
            pet__name = form.cleaned_data.get('pet__name', '')
            visits = visits.filter(available_date__date__icontains=available_date__date, pet__name__icontains=pet__name)
        ctx = {'form': form, 'list_elements': visits}
        return render(request, 'OYP/visits_list_elements.html', ctx)


class VisitDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        visit = Visit.objects.get(pk=pk)
        ctx = {'visit': visit}
        return render(request, 'OYP/visit_detail.html', ctx)


class DeleteVisitView(LoginRequiredMixin, View):
    def get(self, request, pk):
        visit = Visit.objects.get(pk=pk)
        ctx = {'visit': visit}
        return render(request, 'OYP/visit_delete_conf.html', ctx)

    def post(self, request, pk):
        visit = Visit.objects.get(pk=pk)
        visit.delete()
        return redirect('visits_list')
