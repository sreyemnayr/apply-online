import uuid
from django.db import models
from django.contrib.auth import get_user_model
from field_history.tracker import FieldHistoryTracker


class Action(models.Model):
    STARTED_APPLICATION = 0
    COMPLETED_APPLICATION = 1
    APPLICATION_REVIEWED = 2
    SCHEDULED_TOUR = 3
    COMPLETED_TOUR = 4
    TOUR_FOLLOWUP = 5
    PREPARED_CONTRACT = 6
    SENT_CONTRACT = 7
    RETURNED_CONTRACT = 8
    EMAIL = 90
    PHONE_CALL = 91
    MAILING = 92
    OTHER = 99
    ACTION_CHOICES = (
        (STARTED_APPLICATION, 'Started Application'),
        (COMPLETED_APPLICATION, 'Completed Application'),
        (APPLICATION_REVIEWED, 'Reviewed Application'),
        (SCHEDULED_TOUR, 'Tour Scheduled'),
        (COMPLETED_TOUR, 'Tour Completed'),
        (TOUR_FOLLOWUP, 'Tour Follow-Up'),
        (PREPARED_CONTRACT, 'Prepared Contract'),
        (SENT_CONTRACT, 'Sent Contract'),
        (RETURNED_CONTRACT, 'Contract Returned'),
        (EMAIL, 'Email Communication'),
        (PHONE_CALL, 'Phone Call'),
        (MAILING, 'Physical Mailing'),
        (OTHER, 'Other'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.IntegerField('Type of Action', choices=ACTION_CHOICES, default=OTHER)
    date = models.DateTimeField('Date/Time')
    description = models.CharField('Notes', max_length=254, blank=True)
    # user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, null=True)

    field_history = FieldHistoryTracker(['description'])
