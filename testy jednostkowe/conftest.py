from datetime import datetime, time

import pytest
from django.contrib.auth.models import User

from organize_your_pet.models import Pet, Clinic, Doctor, AvailableDate, Visit


@pytest.fixture
def user():
    return User.objects.create(username='test')


@pytest.fixture
def pet():
    x = [
        Pet.objects.create(name='Azor', species='Pies', breed='Mieszaniec', gender='Samiec', birth_date=2022-12-20,
                                weight=2, chip=True),
        Pet.objects.create(name='Kazor', species='Pies', breed='Mieszaniec', gender='Samica', birth_date=2022-10-28,
                                weight=5, chip=False)]
    return x


@pytest.fixture
def clinic():
    x = [
        Clinic.objects.create(name='Vetka', address='ul.Główna 7', city='Wiskitki', phone_number=555-369-285),
        Clinic.objects.create(name='Beatka', address='ul.Górna 157', city='Warszawa', phone_number=575-969-277)
    ]
    return x


@pytest.fixture
def doctor(clinic):
    x = [
        Doctor.objects.create(first_name='Adam', last_name='Azorkiewicz', specialization='Ortopeda', clinic_id=clinic[0].id),
        Doctor.objects.create(first_name='Kamil', last_name='Azork', specialization='Okulista', clinic_id=clinic[0].id),
        Doctor.objects.create(first_name='Abraham', last_name='Kiełkiewicz', specialization='Internista', clinic_id=clinic[0].id),
        Doctor.objects.create(first_name='Anna', last_name='Azot', specialization='Ortopeda', clinic_id=clinic[1].id),
        Doctor.objects.create(first_name='Alina', last_name='Bełkiewicz', specialization='Okulista', clinic_id=clinic[1].id),
        Doctor.objects.create(first_name='Adam', last_name='Tramtyn', specialization='Internista', clinic_id=clinic[1].id),
    ]
    return x


@pytest.fixture
def available_date(doctor):
    x = [
        AvailableDate.objects.create(date=2024-1-30, start_time=time(15,30), end_time=time(16, 00), clinic_id=doctor[0].clinic_id, doctor_id=doctor[0].id),
        AvailableDate.objects.create(date=2024-1-30, start_time=time(15,30), end_time=time(16, 00), clinic_id=doctor[1].clinic_id, doctor_id=doctor[1].id),
        AvailableDate.objects.create(date=2024-1-30, start_time=time(16,30), end_time=time(17, 00), clinic_id=doctor[2].clinic_id, doctor_id=doctor[2].id),
        AvailableDate.objects.create(date=2024-1-30, start_time=time(16,30), end_time=time(17, 00), clinic_id=doctor[3].clinic_id, doctor_id=doctor[3].id),
        AvailableDate.objects.create(date=2024-1-30, start_time=time(15,30), end_time=time(16, 00), clinic_id=doctor[4].clinic_id, doctor_id=doctor[4].id),
        AvailableDate.objects.create(date=2024-1-30, start_time=time(15,30), end_time=time(16, 00), clinic_id=doctor[5].clinic_id, doctor_id=doctor[5].id),
        AvailableDate.objects.create(date=2024-1-31, start_time=time(14,30), end_time=time(15, 00), clinic_id=doctor[0].clinic_id, doctor_id=doctor[0].id),
    ]
    return x


@pytest.fixture
def visit(available_date, pet):
    x = [
        Visit.objects.create(description='łapaała', available_date_id=available_date[0].id, pet_id=pet[0].id),
        Visit.objects.create(description='łapaała', available_date_id=available_date[1].id, pet_id=pet[1].id),
        Visit.objects.create(description='łapaała', available_date_id=available_date[2].id, pet_id=pet[0].id),
        Visit.objects.create(description='łapaała', available_date_id=available_date[3].id, pet_id=pet[1].id),
    ]
    return x