from datetime import datetime, time, date

import pytest
from django.contrib.auth.models import User

from organize_your_pet.models import Pet, Clinic, Doctor, AvailableDate, Visit


@pytest.fixture
def user():
    return User.objects.create()


@pytest.fixture
def pets(user):
    x = [
        Pet.objects.create(name='Azor', species='dog', other_species='brak', breed='Mieszaniec', gender='male',
                           birth_date=date(2022, 12, 20), weight=2, chip=True, owner=user),
        Pet.objects.create(name='Kazor', species='cat', other_species='brak', breed='Mieszaniec', gender='female',
                           birth_date=date(2022, 10, 28), weight=5, chip=False, owner=user)]
    return x


@pytest.fixture
def clinics():
    x = [
        Clinic.objects.create(name='Vetka', address='ul.Główna 7', city='Wiskitki', phone_number=555369285),
        Clinic.objects.create(name='Beatka', address='ul.Górna 157', city='Warszawa', phone_number=575969277)
    ]
    return x


@pytest.fixture
def doctors(clinics):
    x = [
        Doctor.objects.create(first_name='Adam', last_name='Azorkiewicz', specialization='Ortopeda',
                              clinic_id=clinics[0].id),
        Doctor.objects.create(first_name='Kamil', last_name='Azork', specialization='Okulista',
                              clinic_id=clinics[0].id),
        Doctor.objects.create(first_name='Abraham', last_name='Kiełkiewicz', specialization='Internista',
                              clinic_id=clinics[0].id),
        Doctor.objects.create(first_name='Anna', last_name='Azot', specialization='Ortopeda',
                              clinic_id=clinics[1].id),
        Doctor.objects.create(first_name='Alina', last_name='Bełkiewicz', specialization='Okulista',
                              clinic_id=clinics[1].id),
        Doctor.objects.create(first_name='Adam', last_name='Tramtyn', specialization='Internista',
                              clinic_id=clinics[1].id),
    ]
    return x


@pytest.fixture
def available_dates(doctors):
    x = [
        AvailableDate.objects.create(date=date(2024, 1, 30), start_time=time(15,30),
                                     end_time=time(16, 00), clinic_id=doctors[0].clinic_id,
                                     doctor_id=doctors[0].id),
        AvailableDate.objects.create(date=date(2024, 1, 30), start_time=time(15,30),
                                     end_time=time(16, 00), clinic_id=doctors[1].clinic_id,
                                     doctor_id=doctors[1].id),
        AvailableDate.objects.create(date=date(2024, 1, 30), start_time=time(16,30),
                                     end_time=time(17, 00), clinic_id=doctors[2].clinic_id,
                                     doctor_id=doctors[2].id),
        AvailableDate.objects.create(date=date(2024, 1, 30), start_time=time(16,30),
                                     end_time=time(17, 00), clinic_id=doctors[3].clinic_id,
                                     doctor_id=doctors[3].id),
        AvailableDate.objects.create(date=date(2024, 1, 30), start_time=time(15,30),
                                     end_time=time(16, 00), clinic_id=doctors[4].clinic_id,
                                     doctor_id=doctors[4].id),
        AvailableDate.objects.create(date=date(2024, 1, 30), start_time=time(15,30),
                                     end_time=time(16, 00), clinic_id=doctors[5].clinic_id,
                                     doctor_id=doctors[5].id),
        AvailableDate.objects.create(date=date(2024, 1, 30), start_time=time(14,30),
                                     end_time=time(15, 00), clinic_id=doctors[0].clinic_id,
                                     doctor_id=doctors[0].id),
    ]
    return x


@pytest.fixture
def visits(available_dates, pets):
    x = [
        Visit.objects.create(description='łapaała', available_date_id=available_dates[0].id, pet_id=pets[0].id),
        Visit.objects.create(description='łapaała', available_date_id=available_dates[1].id, pet_id=pets[1].id),
        Visit.objects.create(description='łapaała', available_date_id=available_dates[2].id, pet_id=pets[0].id),
        Visit.objects.create(description='łapaała', available_date_id=available_dates[3].id, pet_id=pets[1].id),
    ]
    return x
