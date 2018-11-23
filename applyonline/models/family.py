import uuid
from django.db import models
from address.models import AddressField
from phone_field import PhoneField


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
    preferred_name = models.CharField('Preferred Name', max_length=50, blank=True)
    last_name = models.CharField('Last Name', max_length=50)
    dob = models.DateField('Date of Birth', null=True)
    relationship = models.CharField('Relationship', max_length=2, choices=RELATIONSHIP_CHOICES, default=LEGALGUARDIAN)
    mobile_phone = PhoneField('Mobile Phone', blank=True)
    work_phone = PhoneField('Work Phone', blank=True)
    schools_attended = models.ManyToManyField('OtherSchool')
    hometown = models.CharField('Hometown', max_length=50, blank=True)
    employer = models.CharField('Employer', max_length=50, blank=True)
    job_title = models.CharField('Job Title', max_length=50, blank=True)


class Sibling(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField('First Name', max_length=50)
    dob = models.DateField('Date of Birth', null=True)
    school = models.ForeignKey('OtherSchool', on_delete=models.PROTECT, null=True)


class Family(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('First Name', max_length=50)
    students = models.ManyToManyField('Student')
    parents = models.ManyToManyField('Parent')
    connections = models.BooleanField('Connections to school?', default=False)
    connections_more = models.TextField('More info', blank=True)
    address = AddressField(on_delete=models.CASCADE, null=-True)

