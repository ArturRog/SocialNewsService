# -*- coding: utf-8 -*-

from django.forms import ModelForm
from posts.models import Post, Comment
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
        # labels = {
        #     'title': _('Tytuł'),
        #     'body': _('Treść'),
        #     'picture': _('Zdjęcie'),
        #     'original_url': _('Źródło newsa'),
        #     'category': _('Kategoria'),
        #
        # }
        # help_texts = {
        #     'title': _('Zwięzły tytuł newsa.'),
        #     'body': _('Treść newsa.'),
        #     'original_url': _('Link do oryginalnego źródła z którego pochodzi news.'),
        #     'category': _('Kategoria, do której należy news.'),
        # }
        # error_messages = {
        #     'name': {
        #         'max_length': _("This writer's name is too long."),
        #     },
        # }

