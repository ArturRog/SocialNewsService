# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.test import TestCase

from category.models import Category
from posts.models import Post, Comment, Report, Report_Comment
from posts.views import count_comments


class PostTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.category = Category.objects.create(category_name='Category for test comments', description='description',
                                                owner=self.user)
        self.new_post_url = '/new_post/'
        self.edit_post_url = '/edit_post/{}/'
        self.post_form = {
            'title': 'title',
            'body': 'body',
            'original_url': 'https://docs.djangoproject.com/en/1.10/topics/testing/',
            'category': self.category.id
        }

    def test_new_post_user_logged_in(self):
        self.client.force_login(self.user)
        self.client.post(self.new_post_url, self.post_form)
        is_added = Post.objects.all().count() == 1
        self.assertTrue(is_added)
        post = Post.objects.all()[0]
        self.assertEqual(post.author, self.user)

    def test_new_post_user_not_logged_in(self):
        self.client.post(self.new_post_url, self.post_form)
        is_not_added = Post.objects.all().count() == 0
        self.assertTrue(is_not_added)

    def test_edit_post_user_logged_in(self):
        old_category = Category.objects.create(category_name='old category', description='old category', owner=self.user)
        post = Post.objects.create(title='old_title', body='old_body', author=self.user, category=old_category,
                                   original_url='https://docs.djangoproject.com/en/1.10/topics/testing/old_url/')
        self.client.force_login(self.user)
        self.client.post(self.edit_post_url.format(post.id), self.post_form)
        post = Post.objects.get(id=post.id)
        self.assertEqual(post.title, self.post_form['title'])
        self.assertEqual(post.body, self.post_form['body'])
        self.assertEqual(post.category.id, self.post_form['category'])
        self.assertEqual(post.original_url, self.post_form['original_url'])

    def test_edit_post_user_not_logged_in(self):
        old_category = Category.objects.create(category_name='old category', description='old category', owner=self.user)
        post = Post.objects.create(title='old_title', body='old_body', author=self.user, category=old_category,
                                   original_url='https://docs.djangoproject.com/en/1.10/topics/testing/old_url/')
        self.client.post(self.edit_post_url.format(post.id), self.post_form)
        post = Post.objects.get(id=post.id)
        self.assertNotEqual(post.title, self.post_form['title'])
        self.assertNotEqual(post.body, self.post_form['body'])
        self.assertNotEqual(post.category.id, self.post_form['category'])
        self.assertNotEqual(post.original_url, self.post_form['original_url'])


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
        response = c.post('/comments/show-comments/{}/'.format(self.post.id))
        self.assertEqual(response.status_code, HttpResponse.status_code)
        response = c.post('/comments/show-comments/{}/{}/'.format(self.post.id, self.parent1.id))
        self.assertEqual(response.status_code, HttpResponse.status_code)
        response = c.post('/comments/show-comments/{}/-1'.format(self.post.id))
        self.assertEqual(response.status_code, HttpResponseNotFound.status_code)
        response = c.post('/comments/show-comments/-1/')
        self.assertEqual(response.status_code, HttpResponseNotFound.status_code)
        response = c.post('/comments/show-comments/-1/-1/')
        self.assertEqual(response.status_code, HttpResponseNotFound.status_code)

        parents_sorted = list()
        parents_sorted.append(self.parent1)
        parents_sorted.append(self.parent2)
        parents_sorted.sort(key=lambda x: x.publication_date, reverse=True)
        children_sorted = list()
        children_sorted.append(self.sub1)
        children_sorted.append(self.sub2)
        children_sorted.sort(key=lambda x: x.publication_date, reverse=True)
        response = c.post('/comments/show-comments/{}/'.format(self.post.id))
        self.assertTrue(list(response.context['comments']) == parents_sorted)
        response = c.post('/comments/show-comments/{}/{}/'.format(self.post.id, self.parent1.id))
        self.assertTrue(list(response.context['comments']) == children_sorted)

    def test_new_comment_user_logged_in(self):
        c = self.client
        c.force_login(self.user)
        url = '/comments/new_comment/{}/{}/'.format(self.post.id, self.parent2.id)
        body = 'body of new_sub_comment'
        form_data = {'body': body}
        c.post(url, form_data)
        is_added = Comment.objects.filter(post=self.post, parent=self.parent2, body=body).count() == 1
        self.assertTrue(is_added)
        comment = Comment.objects.filter(post=self.post, parent=self.parent2, body=body).first()
        self.assertEqual(comment.author, self.user)

    def test_new_comment_user_not_logged_in(self):
        url = '/comments/new_comment/{}/{}/'.format(self.post.id, self.parent2.id)
        body = 'body of new_sub_comment'
        form_data = {'body': body}
        self.client.post(url, form_data)
        is_not_added = Comment.objects.filter(post=self.post, parent=self.parent2, body=body).count() == 0
        self.assertTrue(is_not_added)


class MakeReportTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.category = Category.objects.create(category_name='Category for test comments', description='description',
                                                owner=self.user)
        self.post = Post.objects.create(title='title', body='body', author=self.user, category=self.category,
                                        original_url='https://docs.djangoproject.com/en/1.10/topics/testing/')
        self.comment = Comment.objects.create(post=self.post, body='body', author=self.user)
        self.url_post_report = '/report/{}/{}'.format(self.post.id, 1)
        self.url_comment_report = '/report_comment/{}/{}/'.format(self.comment.id, 1)

    def test_make_post_report_user_logged_in(self):
        self.client.force_login(self.user)
        self.client.get(self.url_post_report)
        self.assertEqual(Report.objects.count(), 1)

    def test_make_post_report_user_not_logged_in(self):
        self.client.get(self.url_post_report)
        self.assertEqual(Report.objects.count(), 0)

    def test_make_comment_report_user_logged_in(self):
        self.client.force_login(self.user)
        self.client.get(self.url_comment_report)
        self.assertEqual(Report.objects.count(), 1)

    def test_make_comment_report_user_not_logged_in(self):
        self.client.get(self.url_comment_report)
        self.assertEqual(Report.objects.count(), 0)


class ShowReportTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.category = Category.objects.create(category_name='Category for test comments', description='description',
                                                owner=self.user)
        self.post = Post.objects.create(title='title', body='body', author=self.user, category=self.category,
                                        original_url='https://docs.djangoproject.com/en/1.10/topics/testing/')
        self.comment = Comment.objects.create(post=self.post, body='body', author=self.user)
        self.post_url = '/reports/'
        self.comment_url = '/reports_comment/'

    def test_show_post_report(self):
        self.client.force_login(self.user)
        Report.objects.create(post=self.post, message=1)
        Report.objects.create(post=self.post, message=2)
        all_reports = list(Report.objects.all())
        context_reports = list(self.client.get(self.post_url).context['reports'])
        self.assertEqual(context_reports, all_reports)

    def test_show_comment_report(self):
        self.client.force_login(self.user)
        Report_Comment.objects.create(comment=self.comment, message=1)
        Report_Comment.objects.create(comment=self.comment, message=2)
        all_reports = list(Report_Comment.objects.all())
        context_reports = list(self.client.get(self.comment_url).context['reports'])
        self.assertEqual(context_reports, all_reports)
