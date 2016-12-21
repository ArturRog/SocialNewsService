from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    is_original = models.BooleanField(default=False)  # true dla podstawowych kategorii
    owner = models.ForeignKey(User, related_name="category_owner", blank=True, null=True,
                              default=None)  # kto zalozyl, dla podstawowych None

    def __str__(self):
        return "{0} - {1}".format(self.category_name, self.description).encode('ascii', errors='replace')
