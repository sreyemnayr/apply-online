import uuid
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

from applyonline.models import Parent, Family


@python_2_unicode_compatible
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey('applyonline.Parent', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.profile:
            self.profile, created = Parent.objects.get_or_create(email=self.email)
            if created:
                family = Family.objects.create()
                family.parents.add(self.profile)
        super().save(*args, **kwargs)



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
