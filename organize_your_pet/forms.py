from time import timezone

from django import forms
from django.core.exceptions import ValidationError

from organize_your_pet.models import Pet, AvailableDate, Visit


class AddPetForm(forms.ModelForm):
    species = forms.ChoiceField(choices=[
        ('dog', 'Pies'),
        ('cat', 'Kot'),
        ('parrot', 'Papuga'),
        ('ferret', 'Fretka'),
        ('rabbit', 'Królik'),
        ('rodent', 'Gryzoń'),
        ('other', 'Inny')
    ], widget=forms.Select(attrs={'class': 'form-control'}))
    gender = forms.ChoiceField(choices=[
        ('male', 'Samiec'),
        ('female', 'Samica')
    ], widget=forms.Select(attrs={'class': 'form-control'}))
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}))
    weight = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Pet
        exclude = ('owner',)
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}),
                   'other_species': forms.TextInput(attrs={'class': 'form-control'}),
                   'breed': forms.TextInput(attrs={'class': 'form-control'}),
                   'chip': forms.CheckboxInput}

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        birth_date = cleaned_data.get('birth_date')
        species = cleaned_data.get('species')
        other_species = cleaned_data.get('other_species')
        gender = cleaned_data.get('gender')
        breed = cleaned_data.get('breed')
        weight = cleaned_data.get('weight')
        chip = cleaned_data.get('chip')
        existing_pet = Pet.objects.filter(name=name, birth_date=birth_date, species=species, other_species=other_species,
                                          gender=gender, breed=breed, weight=weight, chip=chip).first()
        if existing_pet:
            raise ValidationError('Podane zwierzę już istnieje')

        return cleaned_data


class PetSearchForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ('name',)
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'})}


class BookAppointmentForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = '__all__'
        # widgets =

    def __init__(self, user, doctor, clinic, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pet'].queryset = Pet.objects.filter(owner=user)
        self.fields['available_date'].queryset = AvailableDate.objects.filter(doctor=doctor, clinic=clinic, is_reserved=False)