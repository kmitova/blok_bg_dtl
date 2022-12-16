from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models

from core.validators import validate_building_code_length


class AppUser(AbstractUser):

    NAME_MAX_LEN = 45
    NAME_MIN_LEN = 2

    first_name = models.CharField(
        max_length=NAME_MAX_LEN,
        validators=(
            validators.MinLengthValidator(NAME_MIN_LEN),
        ),
        null=False,
        blank=True
    )

    last_name = models.CharField(
        max_length=NAME_MAX_LEN,
        validators=(
            validators.MinLengthValidator(NAME_MIN_LEN),
        ),
        null=False,
        blank=True
    )

    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )

    building_code = models.IntegerField(
        validators=(
            validate_building_code_length,
        ),
        null=False,
        blank=False,
    )

    apartment_number = models.CharField(
        default='',
        max_length=20,
        null=True,
        blank=True,
    )

    is_admin = models.BooleanField(
        null=True,
        blank=True,
        default=False
    )

    admin_code = models.CharField(
        max_length=5,
        null=True,
        blank=True,
    )

    profile_picture = models.ImageField(
        upload_to='images/',
        default='images/blank-profile-picture.png',
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

