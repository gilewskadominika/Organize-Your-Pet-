import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from accounts.forms import RegistrationForm, LoginForm
from organize_your_pet.forms import AddPetForm, BookAppointmentForm
from organize_your_pet.models import Pet, Clinic, Doctor, AvailableDate, Visit

# sprawdzenie fixtures


@pytest.mark.django_db
def test_pet_count(pets):
    x = Pet.objects.all()
    assert x.count() == 2


@pytest.mark.django_db
def test_clinic_count(clinics):
    x = Clinic.objects.all()
    assert x.count() == 2


@pytest.mark.django_db
def test_doctor_count(doctors):
    x = Doctor.objects.all()
    assert x.count() == 6


@pytest.mark.django_db
def test_available_date_count(available_dates):
    x = AvailableDate.objects.all()
    assert x.count() == 7


@pytest.mark.django_db
def test_visit_count(visits):
    x = Visit.objects.all()
    assert x.count() == 4

# ----------------------------------------------------------------


@pytest.mark.django_db
def test_registration_user_get():
    client = Client()
    url = reverse('registration_view')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], RegistrationForm)


@pytest.mark.django_db
def test_registration_user_post():
    client = Client()
    url = reverse('registration_view')
    data = {
        'username': 'kazzzzziu',
        'first_name': 'Dupa',
        'last_name': 'DupaDupa',
        'email': 'ziom@wp.pl',
        'password': 'DupaDupa',
        're_password': 'DupaDupa',
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('dashboard')


@pytest.mark.django_db
def test_registration_user_if_login(user):
    client = Client()
    client.force_login(user)
    url = reverse('registration_view')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('dashboard')

# ----------------------------------------------------------------


@pytest.mark.django_db
def test_login_user_get():
    client = Client()
    url = reverse('login_view')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], LoginForm)


# @pytest.mark.django_db
# def test_login_user_post(user):
#     user = User.objects.first()
#     client = Client()
#     url = reverse('login_view')
#     data = {
#         'username': 'test',
#         'password': 'DupaDupa'
#     }
#     response = client.post(url, data)
#     assert user.is_authenticated
#     assert response.status_code == 302
    # assert response.url == reverse('dashboard')


@pytest.mark.django_db
def test_login_user_if_login(user):
    client = Client()
    client.force_login(user)
    url = reverse('login_view')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('dashboard')

# ----------------------------------------------------------------


@pytest.mark.django_db
def test_logout_user_not_login():
    client = Client()
    url = reverse('logout_view')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login_view'))


@pytest.mark.django_db
def test_logout_user(user):
    client = Client()
    client.force_login(user)
    url = reverse('logout_view')
    response = client.get(url)
    assert response.status_code == 302
    assert '_auth_user_id' not in client.session
    assert response.url == reverse('index')

# ----------------------------------------------------------------


@pytest.mark.django_db
def test_profil_view_if_login(user):
    client = Client()
    client.force_login(user)
    url = reverse('profile_view')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['username'] == user.username


@pytest.mark.django_db
def test_profil_view_not_login():
    client = Client()
    url = reverse('profile_view')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login_view'))

# ----------------------------------------------------------------


@pytest.mark.django_db
def test_profil_edit_get(user):
    user = User.objects.first()
    client = Client()
    client.force_login(user)
    url = reverse('profile_edit_view', kwargs={'pk': user.pk})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_profil_edit_post(user):
    user = User.objects.first()
    client = Client()
    client.force_login(user)
    data = {
        'username': 'kaziu'
    }
    url = reverse('profile_edit_view', kwargs={'pk': user.pk})
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('profile_view')
    assert User.objects.get(username=data['username'])

# ----------------------------------------------------------------


@pytest.mark.django_db
def test_index_view_not_login():
    client = Client()
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_index_view_if_login(user):
    client = Client()
    client.force_login(user)
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('dashboard')

# ----------------------------------------------------------------


@pytest.mark.django_db
def test_about_view_not_login():
    client = Client()
    url = reverse('about')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_about_view_if_login(user):
    client = Client()
    client.force_login(user)
    url = reverse('about')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('dashboard')

# ----------------------------------------------------------------


@pytest.mark.django_db
def test_dashboard_view_not_login():
    client = Client()
    url = reverse('dashboard')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login_view'))


@pytest.mark.django_db
def test_dashboard_view_if_login(user, visits):
    visit = Visit.objects.filter(pet__owner=user).order_by('available_date__date').first()
    client = Client()
    client.force_login(user)
    url = reverse('dashboard')
    response = client.get(url)
    assert response.status_code == 200
    assert Visit.objects.filter(pet__owner=user).order_by('available_date__date').first() == visit

# ----------------------------------------------------------------


@pytest.mark.django_db
def test_add_pet_get(user):
    client = Client()
    client.force_login(user)
    url = reverse('add_pet')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AddPetForm)


@pytest.mark.django_db
def test_add_pet_post(user):
    client = Client()
    client.force_login(user)
    url = reverse('add_pet')
    data = {
        'name': 'Azor',
        'species': 'dog',
        'breed': 'Mieszaniec',
        'gender': 'male',
        'birth_date': '2022-12-20',
        'weight': 2.0,
        'chip': True
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('pets_list')
    assert Pet.objects.get(name=data['name'],
                           species=data['species'],
                           breed=data['breed'],
                           gender=data['gender'],
                           birth_date=data['birth_date'],
                           weight=data['weight'],
                           chip=data['chip'])


@pytest.mark.django_db
def test_add_pet_not_login():
    client = Client()
    url = reverse('add_pet')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login_view'))

# ----------------------------------------------------------------


@pytest.mark.django_db
def test_list_pets(pets, user):
    client = Client()
    client.force_login(user)
    url = reverse('pets_list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['list_elements'].count() == len(pets)
    for pet in pets:
        assert pet in response.context['list_elements']


@pytest.mark.django_db
def test_search_pet(pets, user):
    client = Client()
    client.force_login(user)
    url = reverse('pets_list')
    url = f'{url}?name=k'
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['list_elements'].count() == 1
    assert response.context['list_elements'][0] == pets[1]


@pytest.mark.django_db
def test_list_pets_not_login():
    client = Client()
    url = reverse('pets_list')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login_view'))

# ----------------------------------------------------------------


@pytest.mark.django_db
def test_detail_pet(user, pets):
    pet = Pet.objects.first()
    client = Client()
    client.force_login(user)
    url = reverse('pet_info', kwargs={'pk': pet.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['pet'] == pet


@pytest.mark.django_db
def test_detail_pet_not_login(pets):
    pet = Pet.objects.first()
    client = Client()
    url = reverse('pet_info', kwargs={'pk': pet.pk})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login_view'))


# ----------------------------------------------------------------


@pytest.mark.django_db
def test_modify_pet_get(user, pets):
    pet = Pet.objects.first()
    client = Client()
    client.force_login(user)
    url = reverse('modify_pet', kwargs={'pk': pet.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AddPetForm)


@pytest.mark.django_db
def test_modify_pet_post(user, pets):
    pet = Pet.objects.first()
    client = Client()
    client.force_login(user)
    url = reverse('modify_pet', kwargs={'pk': pet.pk})
    new_data = {
        'name': 'Jezor',
        'species': 'cat',
        'breed': 'Mieszaniec',
        'gender': 'male',
        'birth_date': '2022-12-20',
        'weight': 2.0,
        'chip': True
    }
    response = client.post(url, new_data)
    assert response.status_code == 302
    assert response.url == reverse('pet_info', kwargs={'pk': pet.pk})
    assert Pet.objects.get(name=new_data['name'],
                           species=new_data['species'],
                           breed=new_data['breed'],
                           gender=new_data['gender'],
                           birth_date=new_data['birth_date'],
                           weight=new_data['weight'],
                           chip=new_data['chip'])


@pytest.mark.django_db
def test_detail_pet_not_login(pets):
    pet = Pet.objects.first()
    client = Client()
    url = reverse('modify_pet', kwargs={'pk': pet.pk})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login_view'))

# ----------------------------------------------------------------


@pytest.mark.django_db
def test_delete_visit_get(pets, user):
    pet = Pet.objects.first()
    client = Client()
    client.force_login(user)
    url = reverse('delete_pet', kwargs={'pk': pet.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['pet'] == pet


@pytest.mark.django_db
def test_delete_pet_post(user, pets):
    pet = Pet.objects.first()
    client = Client()
    client.force_login(user)
    url = reverse('delete_pet', kwargs={'pk': pet.pk})
    response = client.post(url)
    assert response.status_code == 302
    pet_pks = [pet.pk for pet in Pet.objects.all()]
    assert pet.pk not in pet_pks
    assert response.url == reverse('pets_list')


@pytest.mark.django_db
def test_delete_pet_not_login(pets):
    pet = Pet.objects.first()
    client = Client()
    url = reverse('delete_pet', kwargs={'pk': pet.pk})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login_view'))

# ----------------------------------------------------------------


@pytest.mark.django_db
def test_list_clinics(clinics, user):
    client = Client()
    client.force_login(user)
    url = reverse('clinics_list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['list_elements'].count() == len(clinics)
    for clinic in clinics:
        assert clinic in response.context['list_elements']


@pytest.mark.django_db
def test_list_clinics_not_login(clinics):
    client = Client()
    url = reverse('clinics_list')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login_view'))

# ----------------------------------------------------------------


@pytest.mark.django_db
def test_list_doctors(doctors, user, clinics):
    clinic = Clinic.objects.first()
    doctors = Doctor.objects.filter(clinic_id=clinic.pk)
    client = Client()
    client.force_login(user)
    url = reverse('doctors_list', kwargs={'pk': clinic.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['list_elements'].count() == len(doctors)
    assert response.context['clinic'] == clinic
    for doctor in doctors:
        assert doctor in response.context['list_elements']


@pytest.mark.django_db
def test_list_doctors_not_login(clinics):
    client = Client()
    url = reverse('doctors_list', kwargs={'pk': clinics[0].pk})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login_view'))

# ----------------------------------------------------------------


# @pytest.mark.django_db
# def test_doctor_detail_get(doctors, user, clinics):
#     clinic = Clinic.objects.first()
#     doctor = Doctor.objects.filter(clinic_id=clinic.pk).first()
#     client = Client()
#     client.force_login(user)
#     url = reverse('doctors_list', kwargs={'clinic_pk': clinic.pk, 'doctor_pk': doctor.pk})
#     response = client.get(url)
#     assert response.status_code == 200
#     assert isinstance(response.context['form'], BookAppointmentForm)
#
#
# @pytest.mark.django_db
# def test_doctor_detail_post(user, clinics, doctors, pets, available_dates):
#     date = AvailableDate.objects.filter('date').first()
#     pet = Pet.objects.first()
#     clinic = Clinic.objects.first()
#     doctor = Doctor.objects.filter(clinic_id=clinic.pk).first()
#     client = Client()
#     client.force_login(user)
#     data = {
#         'pet': pet,
#         'available_date': [d.id for d in date],
#         'description': 'łapa'
#     }
#     url = reverse('doctors_list', kwargs={'clinic_pk': clinic.pk, 'doctor_pk': doctor.pk})
#     response = client.get(url, data)
#     assert response.status_code == 302
#     assert response.url == reverse('visits_list')
#
#
# @pytest.mark.django_db
# def test_doctor_detail_not_login(clinics, doctors):
#     client = Client()
#     url = reverse('doctors_list', kwargs={'clinic_pk': clinics[0].pk, 'doctor_pk': doctors[0].pk})
#     response = client.get(url)
#     assert response.status_code == 302
#     assert response.url.startswith(reverse('login_view'))

# ----------------------------------------------------------------


@pytest.mark.django_db
def test_list_visits(visits, user):
    client = Client()
    client.force_login(user)
    url = reverse('visits_list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['list_elements'].count() == len(visits)
    for visit in visits:
        assert visit in response.context['list_elements']


@pytest.mark.django_db
def test_list_visits_not_login(visits):
    client = Client()
    url = reverse('visits_list')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login_view'))

# ----------------------------------------------------------------


@pytest.mark.django_db
def test_visit_detail(visits, user):
    visit = Visit.objects.first()
    client = Client()
    client.force_login(user)
    url = reverse('visit_info', kwargs={'pk': visit.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['visit'] == visit


@pytest.mark.django_db
def test_visit_detail_not_login(visits):
    visit = Visit.objects.first()
    client = Client()
    url = reverse('visit_info', kwargs={'pk': visit.pk})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login_view'))

# ----------------------------------------------------------------


@pytest.mark.django_db
def test_delete_visit_get(visits, user):
    visit = Visit.objects.first()
    client = Client()
    client.force_login(user)
    url = reverse('delete_visit', kwargs={'pk': visit.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['visit'] == visit


@pytest.mark.django_db
def test_delete_visit_post(visits, user):
    visit = Visit.objects.first()
    client = Client()
    client.force_login(user)
    url = reverse('delete_visit', kwargs={'pk': visit.pk})
    response = client.post(url)
    assert response.status_code == 302
    visit_pks = [visit.pk for visit in Visit.objects.all()]
    assert visit.pk not in visit_pks
    assert response.url == reverse('visits_list')


@pytest.mark.django_db
def test_delete_visit_not_login(visits):
    visit = Visit.objects.first()
    client = Client()
    url = reverse('delete_visit', kwargs={'pk': visit.pk})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login_view'))
