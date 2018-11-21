import uuid
from django.db import models


class Student(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    NONBINARY = 'X'

    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (NONBINARY, 'Prefer to not answer')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField('First Name', max_length=50)
    preferred_name = models.CharField('Preferred Name', max_length=50)
    middle_name = models.CharField('Middle Name', max_length=50, blank=True, null=True)
    last_name = models.CharField('Last Name', max_length=50)
    dob = models.DateField('Date of Birth')
    gender = models.CharField('Gender', max_length=1, choices=GENDER_CHOICES, default=NONBINARY)
