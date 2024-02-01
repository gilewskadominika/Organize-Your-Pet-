import pytest

from organize_your_pet.models import Pet


@pytest.mark.django_db
def test_pet_count(pet):
    x = Pet.objects.all()
    assert x.count() == 2