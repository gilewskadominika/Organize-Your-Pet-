from datetime import date, datetime

import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from accounts.forms import RegistrationForm
from organize_your_pet.forms import AddPetForm
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

# ----------------------------------------------------------------


@pytest.mark.django_db
def test_add_pet_get(user):
    client = Client()
    client.force_login(user)
    url = reverse('add_pet')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AddPetForm)


# @pytest.mark.django_db
# def test_add_pet_post(user):
#     client = Client()
#     client.force_login(user)
#     url = reverse('add_pet')
#     data = {
#         'name': 'Azor',
#         'species': 'Pies',
#         'breed': 'Mieszaniec',
#         'gender': 'Samiec',
#         'birth_date': '2022-12-20',
#         'weight': 2.0,
#         'chip': True
#     }
#     response = client.post(url, data)
#     assert response.status_code == 302
#     assert response.url == reverse('pets_list')
#     assert Pet.objects.get(name=data['name'],
#                            species=data['species'],
#                            breed=data['breed'],
#                            gender=data['gender'],
#                            birth_date=data['birth_date'],
#                            weight=data['weight'],
#                            chip=data['chip'])


@pytest.mark.django_db
def test_add_pet_not_login():
    client = Client()
    url = reverse('add_pet')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login_view'))

# ----------------------------------------------------------------


# @pytest.mark.django_db
# def test_detail_pet(user, pets):
#     pet = Pet.objects.first()
#     client = Client()
#     client.force_login(user)
#     url = reverse('pet_info', kwargs={'pk': pet.pk})
#     response = client.get(url)
#     # response = client.get(f'/organize_your_pet/pet/{pets.pk}/')
#     assert response.status_code == 200
#     for field in ('name', 'species', 'other_species', 'breed', 'gender', 'birth_date', 'weight', 'chip', 'owner'):
#         assert field in response.data

# ----------------------------------------------------------------


# @pytest.mark.django_db
# def test_modify_pet(user, pets):
#     pet = Pet.objects.first()
#     client = Client()
#     client.force_login(user)
#     url = reverse('modify_pet', kwargs={'pk': pet.pk})
#     response = client.get(url)
#     pet_data = response.data
#     new_pet_name = 'Kaziu'
#     pet_data['name'] = new_pet_name
#     response = client.patch(url)
#     assert response.status_code == 200
#     pet_object = Pet.objects.get(pk=pet.pk)
#     assert pet_object.name == new_pet_name

# ----------------------------------------------------------------


# @pytest.mark.django_db
# def test_delete_pet(user, pets):
#     pet = Pet.objects.first()
#     client = Client()
#     client.force_login(user)
#     url = reverse('delete_pet', kwargs={'pk': pet.pk})
#     response = client.delete(url)
#     assert response.status_code == 204
#     pet_pks = [pet.pk for pet in Pet.objects.all()]
#     assert pet.pk not in pet_pks

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


# @pytest.mark.django_db
# def test_list_doctors(doctors, user):
#     client = Client()
#     client.force_login(user)
#     url = reverse('doctors_list', kwargs={'clinic_id': doctors[0].clinic_id})
#     response = client.get(url)
#     assert response.status_code == 200
#     assert response.context['list_elements'].count() == len(doctors)
#     for doctor in doctors:
#         assert doctor in response.context['list_elements']
#
#
# @pytest.mark.django_db
# def test_list_doctors_not_login(doctors):
#     client = Client()
#     url = reverse('doctors_list', kwargs={'clinic_id': doctors[0].clinic_id})
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


# @pytest.mark.django_db
# def test_visit_detail(visits, user):
#     visit = Visit.objects.first()
#     client = Client()
#     client.force_login(user)
#     url = reverse('visit_info', kwargs={'pk': visit.pk})
#     response = client.get(url)
#     assert response.status_code == 200
#     for field in 'description':
#         assert field in response.data

# ----------------------------------------------------------------


@pytest.mark.django_db
def test_registration_user():
    client = Client()
    url = reverse('registration_view')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], RegistrationForm)


@pytest.mark.django_db
def test_registration_user_if_login(user):
    client = Client()
    client.force_login(user)
    url = reverse('registration_view')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('dashboard'))

# ----------------------------------------------------------------


# @pytest.mark.django_db
# def test_login_user():
#     user = User.objects.create(username='test', password='DupaDupa')
#     client = Client()
#     client.login(username='test', password='DupaDupa')
#     url = reverse('login_view')
#     response = client.post(url)
#     assert response.status_code == 302


@pytest.mark.django_db
def test_login_user_if_login(user):
    client = Client()
    client.force_login(user)
    url = reverse('login_view')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('dashboard'))

# ----------------------------------------------------------------


@pytest.mark.django_db
def test_logout_user_not_login():
    client = Client()
    url = reverse('logout_view')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login_view'))


@pytest.mark.django_db
def test_logout_user():
    user = User.objects.create(username='jajkon', password='Jajkon')
    client = Client(username='jajkon', password='Jajkon')
    client.login()
    url = reverse('logout_view')
    response = client.get(url)
    assert response.status_code == 302
    assert '_auth_user_id' not in client.session


# ----------------------------------------------------------------

