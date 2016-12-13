# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from posts.models import Category


# Create your models here.

class UserProfile(models.Model):
    user = models.ForeignKey(User)
    favorite_categories = models.ManyToManyField(Category)

    def __str__(self):
        return '{0} {1}'.format(self.user.username, self.favorite_categories.all())
