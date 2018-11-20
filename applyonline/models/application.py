from django.db import models


class Application(models.Model):
    name = models.CharField('Name', max_length=50)
