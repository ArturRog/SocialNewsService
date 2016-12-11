# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime


# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=30)
    description = models.CharField(max_length=300, default="Default category description.")
    is_original = models.BooleanField(default=False)  # true dla podstawowych kategorii
    owner = models.ForeignKey(User, related_name="category_owner", blank=True, null=True, default=None)  # kto zalozyl, dla podstawowych None

    def __str__(self):
        return "{0} - {1}".format(self.category_name, self.description).encode('ascii', errors='replace')


class Post(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    author = models.ForeignKey(User, related_name="post_author")
    publication_date = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to='images', blank=True, null=True, default='default_image.svg')
    original_url = models.URLField()
    category = models.ForeignKey(Category)
    votes = models.IntegerField(default=0, validators=[MaxValueValidator(20000), MinValueValidator(0)])

    def get_post_comments(self):
        return Comment.objects.filter(post=self, parent=None)

    def __str__(self):
        return "{0} -- {1} -- {2} -- {3}".format(self.title, self.category.category_name, self.author,
                                                 self.publication_date.strftime("%d/%m/%y")).encode('ascii',
                                                                                                    errors='replace')


class Comment(models.Model):
    post = models.ForeignKey(Post)
    parent = models.ForeignKey("Comment", null=True, default=None, blank=True)
    body = models.TextField()
    author = models.ForeignKey(User, related_name="comment_author")
    publication_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0}: "{1}" >> {2}'.format(self.id, self.body, self.parent)
