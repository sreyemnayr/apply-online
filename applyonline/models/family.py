import uuid
from django.db import models


class Parent(models.Model):
    FATHER = 'F'
    MOTHER = 'M'
    STEPFATHER = 'SF'
    STEPMOTHER = 'SM'
    GRANDMOTHER = 'GM'
    GRANDFATHER = 'GF'
    LEGALGUARDIAN = 'LG'
    AUNT = 'A'
    UNCLE = 'U'
    SIBLING = 'S'
    RELATIONSHIP_CHOICES = (
        (FATHER, 'Father'),
        (MOTHER, 'Mother'),
        (STEPFATHER, 'Step-Father'),
        (STEPMOTHER, 'Step-Mother'),
        (GRANDMOTHER, 'Grandmother'),
        (GRANDFATHER, 'Grandfather'),
        (UNCLE, 'Uncle'),
        (AUNT, 'Aunt'),
        (LEGALGUARDIAN, 'Legal Guardian'),
        (SIBLING, 'Sibling'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField('First Name', max_length=50)
    preferred_name = models.CharField('Preferred Name', max_length=50, blank=True, null=True)
    middle_name = models.CharField('Middle Name', max_length=50, blank=True, null=True)
    last_name = models.CharField('Last Name', max_length=50)
    dob = models.DateField('Date of Birth', null=True)
    relationship = models.CharField('Relationship', max_length=2, choices=RELATIONSHIP_CHOICES, default=LEGALGUARDIAN)


class Family(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('First Name', max_length=50)
    students = models.ManyToManyField('Student')
    parents = models.ManyToManyField('Parent')

