import uuid
from django.db import models
from field_history.tracker import FieldHistoryTracker


class SchoolYear(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    label = models.CharField('Label', max_length=50)
    start = models.DateField('Start')
    end = models.DateField('End')
    open = models.BooleanField('Open for Applications?', default=False)

    field_history = FieldHistoryTracker(['open'])
