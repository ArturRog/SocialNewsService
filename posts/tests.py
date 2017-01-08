# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.http import HttpResponseNotFound
from django.test import TestCase
from posts.models import Post, Comment
from category.models import Category
from posts.views import count_comments
from django.contrib.auth.models import User


class CategoryTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.category = Category.objects.create(category_name='Category1', description='desc', owner=self.user)
        self.category_count = 1
        self.url = '/new_category/'
        self.form = {
            'category_name': 'category_name',
            'description': 'description',
        }

    def test_new_category_user_logged_in(self):
        self.client.force_login(self.user)
        self.client.post(self.url, self.form)
        self.category_count += 1
        is_added = Category.objects.all().count() == self.category_count
        self.assertTrue(is_added)
        name = self.form['category_name']
        description = self.form['description']
        category = Category.objects.filter(owner=self.user, category_name=name, description=description)[0]
        self.assertEqual(category.owner, self.user)

    def test_new_category_user_not_logged_in(self):
        request = self.client.post(self.url, self.form)
        self.assertEqual(request.status_code, HttpResponseNotAllowed.status_code)
        is_not_added = Category.objects.all().count() == self.category_count
        self.assertTrue(is_not_added)

    def test_search_category_existing_name_like(self):
        new_category = Category.objects.create(category_name='Category2', description='desc', owner=self.user)
        self.url = '/search_category/'
        self.form = {
            'search_text': 'Category'
        }
        response = self.client.post(self.url, self.form)
        response_categories = list(response.context['categories'])

        self.category_count = 2
        self.assertEqual(len(response_categories), self.category_count)

        category_sorted = list()
        category_sorted.append(self.category)
        category_sorted.append(new_category)
        category_sorted.sort(key=lambda x: x.category_name)
        self.assertEqual(response_categories, category_sorted)

    def test_search_category_no_existing_name_like(self):
        self.url = '/search_category/'
        self.form = {
            'search_text': 'bleblebleble there is no name like it!'
        }
        response = self.client.post(self.url, self.form)
        response_categories = list(response.context['categories'])
        self.category_count = 0
        self.assertEqual(len(response_categories), self.category_count)


class PostTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.category = Category.objects.create(category_name='Category for test comments', description='description',
                                                owner=self.user)
        self.new_post_url = '/new_post/'
        self.new_post_form = {
            'title': 'title',
            'body': 'body',
            'original_url': 'https://docs.djangoproject.com/en/1.10/topics/testing/',
            'category': self.category.id
        }

    def test_new_post_user_logged_in(self):
        self.client.force_login(self.user)
        self.client.post(self.new_post_url, self.new_post_form)
        is_added = Post.objects.all().count() == 1
        self.assertTrue(is_added)
        post = Post.objects.all()[0]
        self.assertEqual(post.author, self.user)

    def test_new_post_user_not_logged_in(self):
        self.client.post(self.new_post_url, self.new_post_form)
        is_not_added = Post.objects.all().count() == 0
        self.assertTrue(is_not_added)

    def test_show_posts(self):
        # TODO: test show posts for filters
        pass

    def test_show_posts_wrong_data(self):
        # TODO: test
        pass


class CommentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.category = Category.objects.create(category_name='Category for test comments', description='description',
                                                owner=self.user)
        self.post = Post.objects.create(title='Post for test comments', body='Post body', author=self.user,
                                        picture=None,
                                        original_url='https://docs.djangoproject.com/en/1.10/topics/testing/',
                                        category=self.category, votes=200)
        self.parent1 = Comment.objects.create(post=self.post, parent=None, body='Test parent comment', author=self.user)
        self.parent2 = Comment.objects.create(post=self.post, parent=None, body='Test parent comment 2',
                                              author=self.user)
        self.sub1 = Comment.objects.create(post=self.post, parent=self.parent1, body='sub 1', author=self.user)
        self.sub2 = Comment.objects.create(post=self.post, parent=self.parent1, body='sub 2', author=self.user)
        self.parent_1_comment_count = 2
        self.parent_2_comment_count = 0
        self.all_comments_count = 2 + self.parent_1_comment_count + self.parent_2_comment_count

    def test_comment_count_before_new_sub_comments(self):
        self.assertEqual(count_comments(self.post), self.all_comments_count)
        self.assertEqual(count_comments(self.post, self.parent1), self.parent_1_comment_count)
        self.assertEqual(count_comments(self.post, self.parent2), self.parent_2_comment_count)

    def test_comment_count_after_new_sub_comments(self):
        for i in range(10):
            Comment.objects.create(post=self.post, parent=self.parent1, body='Test parent comment ' + str(i),
                                   author=self.user)
            self.parent_1_comment_count += 1
            self.all_comments_count += 1
        for i in range(4):
            Comment.objects.create(post=self.post, parent=self.parent2, body='Test parent comment ' + str(i),
                                   author=self.user)
            self.parent_2_comment_count += 1
            self.all_comments_count += 1
        self.assertEqual(count_comments(self.post), self.all_comments_count)
        self.assertEqual(count_comments(self.post, self.parent1), self.parent_1_comment_count)
        self.assertEqual(count_comments(self.post, self.parent2), self.parent_2_comment_count)

    def test_comment_count_edge_cases(self):
        self.assertEqual(count_comments(None), 0)
        Comment.objects.all().delete()
        self.all_comments_count = 0
        self.assertEqual(count_comments(self.post), self.all_comments_count)

    def test_show_comments(self):
        c = self.client
        response = c.post('/comments/show-comments/' + str(self.post.id) + '/')
        self.assertEqual(response.status_code, HttpResponse.status_code)
        response = c.post('/comments/show-comments/' + str(self.post.id) + '/' + str(self.parent1.id) + '/')
        self.assertEqual(response.status_code, HttpResponse.status_code)
        response = c.post('/comments/show-comments/' + str(self.post.id) + '/-1/')
        self.assertEqual(response.status_code, HttpResponseNotFound.status_code)
        response = c.post('/comments/show-comments/-1/')
        self.assertEqual(response.status_code, HttpResponseNotFound.status_code)
        response = c.post('/comments/show-comments/-1/-1')
        self.assertEqual(response.status_code, HttpResponseNotFound.status_code)

        parents_sorted = list()
        parents_sorted.append(self.parent1)
        parents_sorted.append(self.parent2)
        parents_sorted.sort(key=lambda x: x.publication_date, reverse=True)
        children_sorted = list()
        children_sorted.append(self.sub1)
        children_sorted.append(self.sub2)
        children_sorted.sort(key=lambda x: x.publication_date, reverse=True)
        response = c.post('/comments/show-comments/' + str(self.post.id) + '/')
        self.assertTrue(list(response.context['comments']) == parents_sorted)
        response = c.post('/comments/show-comments/' + str(self.post.id) + '/' + str(self.parent1.id) + '/')
        self.assertTrue(list(response.context['comments']) == children_sorted)

    def test_new_comment_user_logged_id(self):
        c = self.client
        c.force_login(self.user)
        url = '/comments/new_comment/' + str(self.post.id) + '/' + str(self.parent2.id) + '/'
        body = 'body of new_sub_comment'
        form_data = {'body': body}
        c.post(url, form_data)
        is_added = Comment.objects.filter(post=self.post, parent=self.parent2, body=body).count() == 1
        self.assertTrue(is_added)
        comment = Comment.objects.filter(post=self.post, parent=self.parent2, body=body).first()
        self.assertEqual(comment.author, self.user)

    def test_new_comment_user_not_logged_in(self):
        url = '/comments/new_comment/' + str(self.post.id) + '/' + str(self.parent2.id) + '/'
        body = 'body of new_sub_comment'
        form_data = {'body': body}
        self.client.post(url, form_data)
        is_not_added = Comment.objects.filter(post=self.post, parent=self.parent2, body=body).count() == 0
        self.assertTrue(is_not_added)
