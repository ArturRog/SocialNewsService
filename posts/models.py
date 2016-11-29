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
    cathegory = models.CharField(max_length=20)

    def __str__(self):
        return "{0} -- {1} -- {2} -- {3}".format(self.title, self.cathegory, self.author,
                                                 self.publication_date.strftime("%d/%m/%y")).encode('ascii',
                                                                                                    errors='replace')
