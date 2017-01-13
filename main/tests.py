# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.timezone import utc

from category.models import Category
from posts.models import Post
from datetime import datetime, timedelta


class PostFilterTestCase(TestCase):

    def setUp(self):
        now = datetime.now().utcnow().replace(tzinfo=utc)
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.category = Category.objects.create(category_name='Category for test comments', description='description',
                                                owner=self.user)
        post1 = Post.objects.create(title='title1', body='body1', author=self.user, category=self.category,
                                    original_url='https://docs.djangoproject.com/en/1.10/topics/testing/1')
        post1.publication_date = now
        post1.save()
        post2 = Post.objects.create(title='title2', body='body2', author=self.user, category=self.category,
                                    original_url='https://docs.djangoproject.com/en/1.10/topics/testing/2')
        post2.publication_date = now - timedelta(hours=1)
        post2.save()
        post3 = Post.objects.create(title='title3', body='body3', author=self.user, category=self.category,
                                    original_url='https://docs.djangoproject.com/en/1.10/topics/testing/3')
        post3.publication_date = now - timedelta(days=2)
        post3.save()
        post4 = Post.objects.create(title='title4', body='body4', author=self.user, category=self.category,
                                    original_url='https://docs.djangoproject.com/en/1.10/topics/testing/4')
        post4.publication_date = now - timedelta(days=12)
        post4.save()
        post5 = Post.objects.create(title='title5', body='body5', author=self.user, category=self.category,
                                    original_url='https://docs.djangoproject.com/en/1.10/topics/testing/5')
        post5.publication_date = now - timedelta(days=32)
        post5.save()
        self.day_filter = (post1, post2)
        self.week_filter = (post1, post2, post3)
        self.month_filter = (post1, post2, post3, post4, post5)
        self.day_filter_url = '/cat-dzien/'
        self.week_filter_url = '/cat-tydzien/'
        self.month_filter_url = '/cat-month/'

    def test_day_filter(self):
        response = self.client.get(self.day_filter_url)
        self.assertEqual(tuple(response.context['posts']), self.day_filter)

    def test_week_filter(self):
        response = self.client.get(self.week_filter_url)
        self.assertEqual(tuple(response.context['posts']), self.week_filter)

    def test_month_filter(self):
        response = self.client.get(self.month_filter_url)
        self.assertEqual(tuple(response.context['posts']), self.month_filter)

