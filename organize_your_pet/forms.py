from django import forms


class AddPetForm(forms.Form):
    GENDERS = [
        ('male', 'Samiec'),
        ('female', 'Samica'),
    ]
    SPECIES = [
        ('dog', 'Pies'),
        ('cat', 'Kot'),
        ('parrot', 'Papuga'),
        ('ferret', 'Fretka'),
        ('rabbit', 'Królik'),
        ('rodent', 'Gryzoń'),
        ('other', 'Inny')
    ]
    name = forms.CharField(max_length=50)
    species = forms.ChoiceField(choices=SPECIES)
    other_species = forms.CharField(max_length=50, required=False)
    breed = forms.CharField(max_length=50)
    gender = forms.ChoiceField(choices=GENDERS)
    birth_date = forms.DateField(required=False)
    weight = forms.FloatField()
    chip = forms.BooleanField()
