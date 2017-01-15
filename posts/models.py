# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from category.models import Category


class Post(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    author = models.ForeignKey(User, related_name="post_author")
    publication_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    is_modified = models.BooleanField(default=False)
    picture = models.ImageField(upload_to='images', blank=True, null=True)
    original_url = models.URLField()
    category = models.ForeignKey(Category)
    votes = models.IntegerField(default=0, validators=[MaxValueValidator(20000), MinValueValidator(0)])

    def __str__(self):
        return "{0} -- {1} -- {2}".format(self.title, self.author, self.publication_date.strftime("%d/%m/%y"))\
            .encode('utf-8', errors='replace')


class PostVotes(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    vote = models.IntegerField(default=0, validators=[MaxValueValidator(1), MinValueValidator(-1)])


class Comment(models.Model):
    post = models.ForeignKey(Post)
    parent = models.ForeignKey("Comment", null=True, default=None, blank=True)
    body = models.TextField()
    author = models.ForeignKey(User, related_name="comment_author")
    publication_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Autor: {0} id {1}: "{2}" >> {3}'.format(self.author, self.id, self.body, self.parent)\
            .encode('utf-8', errors='replace')


class Report(models.Model):
    post = models.ForeignKey(Post)
    message = models.TextField()
    checked = models.BooleanField(default=False)

    def __str__(self):
        return "{0} --Sprawdzony? {1} -- {2}".format(self.message, self.checked, self.post.title)\
            .encode('utf-8', errors='replace')


class Report_Comment(models.Model):
    comment = models.ForeignKey(Comment)
    message = models.TextField()
    checked = models.BooleanField(default=False)

    def __str__(self):
        return "{0} --Sprawdzony? {1}".format(self.message, self.checked)\
            .encode('utf-8', errors='replace')
