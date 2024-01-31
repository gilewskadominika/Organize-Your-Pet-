from time import timezone

from django import forms

from organize_your_pet.models import Pet, Visit, AvailableDate


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


class PetSearchForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ('name',)
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'})}


class BookAppointmentForm(forms.ModelForm):
    class Meta:
        model = AvailableDate
        fields = '__all__'
        widgets = {
            'clinic': forms.Select(attrs={'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.Select(attrs={'class': 'form-control'}),
            'end_time': forms.Select(attrs={'class': 'form-control'}),
        }