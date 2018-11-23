import uuid
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from dateutil.relativedelta import relativedelta
from decimal import Decimal
from django.db.models.signals import m2m_changed

from field_history.tracker import FieldHistoryTracker


class OtherSchool(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Name', max_length=32, blank=True)


class Application(models.Model):
    GRADE_LEVEL_CHOICES = (
                (-4,'One-year-olds'),
                (-3, 'Two-year-olds'),
                (-2, 'Pre-K 3'),
                (-1, 'Pre-K'),
                (0, 'Kindergarten'),
                (1, '1st Grade'),
                (2, '2nd Grade'),
                (3, '3rd Grade'),
                (4, '4th Grade'),
                (5, '5th Grade'),
                (6, '6th Grade'),
                (7, '7th Grade'),
                (8, '8th Grade'),
    )

    FULL = 8
    HALF = 5
    OTHER = 0

    TIME_CHOICES = (
        (FULL, 'Full Days (7:30-3:30'),
        (HALF, 'Half Days (7:30-12:30'),
        (OTHER, 'Other')
    )

    FIVEDAYS = 5
    THREEDAYS = 3
    TWODAYS = 2

    DAY_CHOICES = (
        (FIVEDAYS, '5 Days (Monday-Friday)'),
        (THREEDAYS, '3 Days (Monday, Wednesday, Friday)'),
        (TWODAYS, '2 Days (Tuesday, Thursday)'),
        (OTHER, 'Other')
    )

    REQUIRED_M2M = ('families')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    student = models.ForeignKey('Student', on_delete=models.PROTECT)
    school_year = models.ForeignKey('SchoolYear', on_delete=models.PROTECT)
    families = models.ManyToManyField('Family')
    complete = models.BooleanField('Completed?', default=False)

    # Form fields
    applying_for = models.IntegerField('Grade level applying for', choices=GRADE_LEVEL_CHOICES, default=999)
    current_grade = models.IntegerField('Current grade level', choices=(*GRADE_LEVEL_CHOICES, (-999, 'No school')), default=999)

    # Scheduling (preschool)
    schedule_time = models.IntegerField('Schedule preference (Times)', choices=TIME_CHOICES, default=0)
    schedule_days = models.IntegerField('Schedule preference (Days)', choices=DAY_CHOICES, default=0)
    schedule_more = models.CharField('Scheduling notes', max_length=254, blank=True)

    # Other school applications
    other_schools = models.ManyToManyField('OtherSchool')

    # Calculated fields
    student_age_months = models.IntegerField('Age in Months (School Year Start)', default=0)
    student_age_years = models.DecimalField('Age in Years (School Year Start)', decimal_places=2, max_digits=5, default=0.0)

    # Overridden save method to calculate things and check for completion
    def save(self, *args, **kwargs):

        rd = relativedelta(self.school_year.start, self.student.dob).normalized()

        self.student_age_months = rd.years * 12 + rd.months
        self.student_age_years = Decimal(rd.years) + Decimal(rd.months) / Decimal(12.0)

        self.complete = True if self.percent_complete == 100 else False

        super().save(*args, **kwargs)

    def complete_incomplete(self):
        incomplete = []
        complete = []
        for field in self._meta.get_fields():
            if field.many_to_many:
                if getattr(self, field.name,None).exists():
                    complete += [field.name]
                else:
                    if field.name in self.REQUIRED_M2M:
                        incomplete += [field.name]
            elif getattr(self, field.name, None) is None:
                incomplete += [field.name]
            else:
                complete += [field.name]

        return complete, incomplete

    @property
    def percent_complete(self):
        complete, incomplete = self.complete_incomplete()
        return int((len(complete) / (len(incomplete) + len(complete))) * 100)

    @property
    def incomplete_fields(self):
        complete, incomplete = self.complete_incomplete()
        return incomplete


@receiver(m2m_changed, sender=Application.families.through)
def save_after_adding(sender, instance=None, action=None, **kwargs):
    if action == "post_add":
        instance.save()
