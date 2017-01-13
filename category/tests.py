# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.test import TestCase
from category.models import Category


class CategoryTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.category = Category.objects.create(category_name='Category1', description='desc', owner=self.user)
        self.category_count = 1
        self.url_new = '/new_category/'
        self.url_search = '/search_category/'
        self.form = {
            'category_name': 'category_name',
            'description': 'description',
        }

    def test_new_category_user_logged_in(self):
        self.client.force_login(self.user)
        self.client.post(self.url_new, self.form)
        self.category_count += 1
        is_added = Category.objects.all().count() == self.category_count
        self.assertTrue(is_added)
        name = self.form['category_name']
        description = self.form['description']
        category = Category.objects.filter(owner=self.user, category_name=name, description=description)[0]
        self.assertEqual(category.owner, self.user)

    def test_new_category_user_not_logged_in(self):
        self.client.post(self.url_new, self.form)
        is_not_added = Category.objects.all().count() == self.category_count
        self.assertTrue(is_not_added)

    def test_search_category_existing_name_like(self):
        new_category = Category.objects.create(category_name='Category2', description='desc', owner=self.user)
        self.form = {
            'search_text': 'Category'
        }
        response = self.client.post(self.url_search, self.form)
        response_categories = list(response.context['categories'])

        self.category_count = 2
        self.assertEqual(len(response_categories), self.category_count)

        category_sorted = list()
        category_sorted.append(self.category)
        category_sorted.append(new_category)
        category_sorted.sort(key=lambda x: x.category_name)
        self.assertEqual(response_categories, category_sorted)

    def test_search_category_no_existing_name_like(self):
        self.form = {
            'search_text': 'bleblebleble there is no name like it!'
        }
        response = self.client.post(self.url_search, self.form)
        response_categories = list(response.context['categories'])
        self.category_count = 0
        self.assertEqual(len(response_categories), self.category_count)
