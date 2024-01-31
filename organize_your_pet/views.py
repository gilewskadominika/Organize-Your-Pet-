from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import UpdateView
from organize_your_pet.forms import AddPetForm, PetSearchForm, BookAppointmentForm
from organize_your_pet.models import Visit, Pet, Clinic, Doctor


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


class ClinicsListView(LoginRequiredMixin, View):
    def get(self, request):
        clinics = Clinic.objects.all()
        ctx = {'list_elements': clinics}
        return render(request, 'OYP/clinics_list_elements.html', ctx)


class DoctorsListView(LoginRequiredMixin, View):
    def get(self, request, pk):
        clinic = Clinic.objects.get(pk=pk)
        doctors = Doctor.objects.filter(clinic_id=clinic.pk)
        ctx = {'clinic': clinic, 'list_elements': doctors}
        return render(request, 'OYP/doctors_list_elements.html', ctx)


class DoctorDetailView(LoginRequiredMixin, View):
    def get(self, request, clinic_pk, doctor_pk):
        form = BookAppointmentForm(user=request.user)
        clinic = Clinic.objects.get(pk=clinic_pk)
        doctor = Doctor.objects.get(pk=doctor_pk)
        ctx = {'clinic_pk': clinic, 'doctor_pk': doctor, 'form': form}
        return render(request, 'OYP/add_form_for_logged_in.html', ctx)

    def post(self, request):
        form = BookAppointmentForm(data=request.POST, user=request.user)
        ctx = {'form': form}
        if form.is_valid():
            visit = form.save(commit=False)
            visit.pet.owner = self.request.user
            visit.save()
            return redirect('visits_list')
        return render(request, 'OYP/add_form_for_logged_in.html', ctx)

# class BookAppointmentView(LoginRequiredMixin, View):
#     def get(self, request):
#         form = BookAppointmentForm(user=request.user)
#         ctx = {'form': form}
#         return render(request, 'OYP/add_form_for_logged_in.html', ctx)
#
#     def post(self, request):
#         form = BookAppointmentForm(data=request.POST, user=request.user)
#         ctx = {'form': form}
#         if form.is_valid():
#             visit = form.save(commit=False)
#             visit.pet.owner = self.request.user
#             visit.save()
#             return redirect('visits_list')
#         return render(request, 'OYP/add_form_for_logged_in.html', ctx)


class VisitsListView(LoginRequiredMixin, View):
    def get(self, request):
        visits = Visit.objects.filter(pet__owner=request.user)
        ctx = {'list_elements': visits}
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
