from django import forms

from organize_your_pet.models import Pet, Visit


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


class AddVisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = '__all__'
        widgets = {
            'available_date': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class VisitSearchForm(forms.ModelForm):
    available_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}))
    pet = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Visit
        fields = ('pet', 'available_date')

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pet__name'].queryset = Pet.objects.filter(owner=user)