# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from posts.models import Category
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class UserProfile(models.Model):
    user = models.ForeignKey(User)
    reputation = models.IntegerField(default=0, validators=[MaxValueValidator(20000), MinValueValidator(0)])
    favorite_categories = models.ManyToManyField(Category)

    def __str__(self):
        return '{0} {1}'.format(self.user.username, self.favorite_categories.all())
