import uuid
from django.db import models
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from django.db.models.signals import m2m_changed

from field_history.tracker import FieldHistoryTracker


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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    student = models.ForeignKey('Student', on_delete=models.PROTECT)
    school_year = models.ForeignKey('SchoolYear', on_delete=models.PROTECT)
    families = models.ManyToManyField('Family')
    complete = models.BooleanField('Completed?', default=False)

    # Form fields
    applying_for = models.IntegerField('Grade level applying for', choices=GRADE_LEVEL_CHOICES)
    current_grade = models.IntegerField('Current grade level', choices=(*GRADE_LEVEL_CHOICES, (-999, 'No school')))


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
                if getattr(self,field.name,None).exists():
                    complete += [field.name]
                else:
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


def m2m_add_collector(sender, **kwargs):
    if kwargs["action"] == "post_add":
        kwargs["instance"].save()


m2m_changed.connect(m2m_add_collector, sender=Application.families.through)
