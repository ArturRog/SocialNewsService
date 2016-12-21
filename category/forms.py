# -*- coding: utf-8 -*-

from django.forms import ModelForm
from category.models import Category
from django.utils.translation import ugettext_lazy as _


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']
        labels = {
            'category_name': _('Nazwa kategorii'),
            'description': _('Opis kategorii'),
        }
        help_texts = {
            'category_name': _('Wprowadz nazwe dla nowej kategorii (bez polskich znakow).'),
            'description': _('Krotki opis nowej kategorii.'),
        }
