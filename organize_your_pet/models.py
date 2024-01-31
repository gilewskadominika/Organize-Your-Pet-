from django.db import models
from django.contrib.auth.models import User


class Pet(models.Model):
    GENDERS = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    SPECIES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('parrot', 'Parrot'),
        ('ferret', 'Ferret'),
        ('rabbit', 'Rabbit'),
        ('rodent', 'Rodent'),
        ('other', 'Other')
    ]
    name = models.CharField(max_length=50, blank=True)
    species = models.CharField(max_length=50, choices=SPECIES, default='other')
    other_species = models.TextField(blank=True, null=True)
    breed = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=GENDERS, default='male')
    birth_date = models.DateField(null=True)
    weight = models.FloatField()
    chip = models.BooleanField(default=False)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.species}{self.other_species})'


class Clinic(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f'{self.name} - {self.city}, {self.address}'


class Doctor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    specialization = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class AvailableDate(models.Model):
    clinic = models.ForeignKey('Clinic', on_delete=models.CASCADE)
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'''Termin w klinice {self.clinic.name}, 
        lekarz przyjmujący {self.doctor}
        dnia {self.date} od {self.start_time} do {self.end_time}.
         .'''


class Visit(models.Model):
    pet = models.ForeignKey('Pet', on_delete=models.CASCADE)
    available_date = models.ForeignKey('AvailableDate', on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f'''Wizyta w klinice {self.available_date.clinic.name} dla {self.pet} odbędzie się {self.available_date.date} 
        o godzinie {self.available_date.start_time}. Przyjmie lekarz {self.available_date.doctor}. 
        Opis wizyty: {self.description}'''
