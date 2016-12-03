from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import datetime


# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    author = models.ForeignKey(User, related_name="post_author")
    publication_date = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to='images', blank=True, null=True, default='default_image.svg')
    original_url = models.URLField()
    category = models.CharField(max_length=20)

    def get_post_comments(self):
        return Comment.objects.filter(post=self, parent=None)

    def __str__(self):
        return "{0} -- {1} -- {2} -- {3}".format(self.title, self.category, self.author,
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

