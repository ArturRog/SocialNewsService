# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.timezone import utc

from category.models import Category
from posts.models import Post
from datetime import datetime, timedelta

from user_profile.models import UserProfile


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


class VotesTestCase(TestCase):

    def setUp(self):
        self.author = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.category = Category.objects.create(category_name='Category for test comments', description='description',
                                                owner=self.author)
        self.post = Post.objects.create(title='title1', body='body1', author=self.author, category=self.category,
                                        original_url='https://docs.djangoproject.com/en/1.10/topics/testing/1')
        self.author_profile = UserProfile.objects.create(user=self.author)
        self.up_vote_url = '/upvote_news/{}/'.format(self.post.id)
        self.down_vote_url = '/downvote_news/{}/'.format(self.post.id)
        self.voting_user = User.objects.create_user('john_voting', 'lennon@voting_thebeatles.com', 'johnpassword')
        self.voting_user_profile = UserProfile.objects.create(user=self.voting_user)

    def test_up_vote_user_logged_in(self):
        self.client.force_login(self.voting_user)
        self.client.get(self.up_vote_url)
        post = Post.objects.get(id=self.post.id)
        self.assertEqual(post.votes, 1)
        self.client.get(self.up_vote_url)
        post = Post.objects.get(id=self.post.id)
        self.assertEqual(post.votes, 1)

    def test_up_vote_user_logged_out(self):
        self.client.get(self.up_vote_url)
        post = Post.objects.get(id=self.post.id)
        self.assertEqual(post.votes, 0)

    def test_down_vote_user_logged_in(self):
        self.client.force_login(self.voting_user)
        self.client.get(self.down_vote_url)
        post = Post.objects.get(id=self.post.id)
        self.assertEqual(post.votes, -1)
        self.client.get(self.down_vote_url)
        post = Post.objects.get(id=self.post.id)
        self.assertEqual(post.votes, -1)

    def test_down_vote_user_logged_out(self):
        self.client.get(self.down_vote_url)
        post = Post.objects.get(id=self.post.id)
        self.assertEqual(post.votes, 0)

    def test_up_down_vote_user_logged_in(self):
        self.client.force_login(self.voting_user)
        self.client.get(self.down_vote_url)
        self.client.get(self.up_vote_url)
        post = Post.objects.get(id=self.post.id)
        self.assertEqual(post.votes, 1)
        self.client.get(self.down_vote_url)
        post = Post.objects.get(id=self.post.id)
        self.assertEqual(post.votes, -1)


class CategoryFilterTestCase(TestCase):

    def setUp(self):
        self.author = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.categories, self.posts = list(), list()
        for i in range(6):
            self.categories.append(Category.objects.create(
                category_name='Category {}'.format(i), description='description {}'.format(i), owner=self.author))
        for i in range(2, 12):
            if i % 2 == 0:
                post = Post.objects.create(title='title {}'.format(i), body='body {}'.format(i), author=self.author,
                                           category=self.categories[0],
                                           original_url='https://docs.djangoproject.com/en/1.10/topics/testing/1')
                self.posts.append(post)
            else:
                Post.objects.create(title='title {}'.format(i), body='body {}'.format(i), author=self.author,
                                    category=self.categories[i/2],
                                    original_url='https://docs.djangoproject.com/en/1.10/topics/testing/1')
        self.category_filter_url = '/category/{}/'.format(self.categories[0].id)

    def test_category_filter(self):
        response = self.client.get(self.category_filter_url)
        self.assertEqual(list(response.context['posts']), self.posts)
