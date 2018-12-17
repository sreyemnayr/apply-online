import uuid
from django.db import models


class Evaluation(models.Model):
    ACCOMPLISHMENT = "A"
    REPEATED_GRADE = "R"
    PSYCH = "P"
    EDUCATIONAL = "E"
    SPEECH = "S"
    OCCUPATIONAL = "O"
    COUNSELOR = "C"
    OTHER = "X"
    EVAL_CHOICES = (
        (ACCOMPLISHMENT, "Accomplishment"),
        (REPEATED_GRADE, "Repeated Grade"),
        (PSYCH, "Psychological Evaluation"),
        (EDUCATIONAL, "Educational Evaluation"),
        (SPEECH, "Speech/Language Evaluation"),
        (OCCUPATIONAL, "Occupational Therapy"),
        (COUNSELOR, "Professional Counseling"),
        (OTHER, "Other"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField("Type", max_length=2, choices=EVAL_CHOICES, default=OTHER)
    date = models.DateField("Date of Birth")
    description = models.CharField("Describe your child", max_length=254, blank=True)


class Student(models.Model):
    MALE = "M"
    FEMALE = "F"
    NONBINARY = "X"

    GENDER_CHOICES = (
        (MALE, "Male"),
        (FEMALE, "Female"),
        (NONBINARY, "Prefer to not answer"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField("First Name", max_length=50)
    preferred_name = models.CharField("Preferred Name", max_length=50)
    middle_name = models.CharField("Middle Name", max_length=50, blank=True, null=True)
    last_name = models.CharField("Last Name", max_length=50)
    dob = models.DateField("Date of Birth")
    gender = models.CharField(
        "Gender", max_length=1, choices=GENDER_CHOICES, default=NONBINARY
    )
    description = models.CharField("Describe your child", max_length=254, blank=True)
    schools_attended = models.ManyToManyField(
        "OtherSchool", related_name="students_attended", blank=True
    )
    current_school = models.ForeignKey(
        "OtherSchool", on_delete=models.PROTECT, null=True, related_name="students_current"
    )
    evaluations = models.ManyToManyField("Evaluation", blank=True)
