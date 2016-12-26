# -*- coding: utf-8 -*-

from django.forms import ModelForm
from posts.models import Post, Comment, Report, ReportMessages
from django.utils.translation import ugettext_lazy as _


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'picture', 'original_url', "category"]
        labels = {
            'title': _('Tytul'),
            'body': _('Tresc'),
            'picture': _('Zdjecie'),
            'original_url': _('Zrodlo newsa'),
            'category': _('Kategoria'),

        }
        help_texts = {
            'original_url': _('Link do oryginalnego zrodla z ktorego pochodzi news.'),
            'category': _('Kategoria, do ktorej nalezy news.'),
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels = {
            'body': _('')
        }


# class ReportForm(ModelForm):
#     class Meta:
#         model = Report
#         fields = ['message']