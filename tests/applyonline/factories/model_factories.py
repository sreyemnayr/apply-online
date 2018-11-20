import random

from factory.django import DjangoModelFactory
import factory

from django.utils import timezone

import applyonline.models


class ApplicationFactory(DjangoModelFactory):
    class Meta:
        model = applyonline.models.Application
