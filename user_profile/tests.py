from django.contrib.auth.models import User
from django.test import TestCase

from category.models import Category
from posts.models import Post, Comment
from user_profile.models import UserProfile


class UserProfileBaseTestCase(TestCase):
    def setUp(self):
        self.other_user = User.objects.create_user('john_other', 'lennon@other.com', 'johnpassword_other')
        self.test_user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        UserProfile.objects.create(user=self.other_user)
        self.user_profile = UserProfile.objects.create(user=self.test_user)
        my_cat1 = Category.objects.create(category_name='cat1', description='desc1', owner=self.test_user)
        my_cat2 = Category.objects.create(category_name='cat2', description='desc2', owner=self.test_user)
        favourite1 = Category.objects.create(category_name='cat3', description='desc3', owner=self.other_user)
        favourite2 = Category.objects.create(category_name='cat4', description='desc4', owner=self.other_user)
        Category.objects.create(category_name='cat5', description='desc5', owner=self.other_user)
        self.user_profile.favorite_categories.add(favourite1)
        self.user_profile.favorite_categories.add(favourite2)
        self.user_profile.save()

        post1 = Post.objects.create(title='title1', body='body1', author=self.test_user, category=favourite1,
                                    original_url='https://docs.djangoproject.com/en/1.10/topics/testing/')
        post2 = Post.objects.create(title='title2', body='body2', author=self.test_user, category=favourite2,
                                    original_url='https://docs.djangoproject.com/en/1.10/topics/testing/')
        post3 = Post.objects.create(title='title3', body='body3', author=self.test_user, category=my_cat1,
                                    original_url='https://docs.djangoproject.com/en/1.10/topics/testing/')
        Post.objects.create(title='title3', body='body3', author=self.other_user, category=favourite2,
                            original_url='https://docs.djangoproject.com/en/1.10/topics/testing/')

        comment1 = Comment.objects.create(post=post1, body='comment', author=self.test_user)
        comment2 = Comment.objects.create(post=post1, body='comment', author=self.test_user)
        Comment.objects.create(post=post1, body='comment', author=self.other_user)

        self.my_categories = [my_cat1, my_cat2]
        self.my_favourite = [favourite1, favourite2]
        self.my_comments = [comment1, comment2]
        self.my_posts = [post1, post2, post3]


class MenuContextTestCase(UserProfileBaseTestCase):

    def setUp(self):
        UserProfileBaseTestCase.setUp(self)
        self.client.force_login(self.test_user)
        self.context = self.client.get('/profile/').context

    def test_my_categories(self):
        self.assertEqual(list(self.context['categories']), self.my_categories)

    def test_favourite_categories(self):
        self.assertEqual(list(self.context['fav_categories']), self.my_favourite)

    def test_user_profile(self):
        self.assertEqual(self.context['user_profile'], self.user_profile)

    def test_comments(self):
        self.assertEqual(list(self.context['comments']), self.my_comments)

    def test_posts(self):
        self.assertEqual(list(self.context['posts']), self.my_posts)


class MyProfileTestCase(UserProfileBaseTestCase):

    def setUp(self):
        UserProfileBaseTestCase.setUp(self)
        self.client.force_login(self.test_user)

    def test_posts_from_category(self):
        cat = self.my_categories[0]
        posts = [self.my_posts[2]]
        context = self.client.get('/my_categories/{}/'.format(cat.id)).context
        self.assertEqual(list(context['posts']), posts)

    def test_my_comments(self):
        context = self.client.get('/my_comments/').context
        self.assertEqual(list(context['comments']), self.my_comments)

    def test_my_posts(self):
        context = self.client.get('/my_posts/').context
        self.assertEqual(list(context['posts']), self.my_posts)

    def test_my_settings(self):
        context = self.client.get('/my_settings/').context
        self.assertEqual(context['current_user'], self.test_user)


class AddToFavouriteTestCase(UserProfileBaseTestCase):

    def setUp(self):
        UserProfileBaseTestCase.setUp(self)
        self.client.force_login(self.test_user)
        self.url = '/add_to_favorites/{}/'

    def test_add_to_favourite(self):
        cat = Category.objects.create(category_name='new_favourite', description='desc5', owner=self.other_user)
        self.my_favourite.append(cat)
        self.client.get(self.url.format(cat.id))
        test_favourite = UserProfile.objects.filter(user=self.test_user).first().favorite_categories.all()
        self.assertEqual(list(test_favourite), self.my_favourite)

    def test_delete_from_favourite(self):
        cat = self.my_favourite[1]
        self.client.get(self.url.format(cat.id))
        self.my_favourite = [self.my_favourite[0]]
        test_favourite = UserProfile.objects.filter(user=self.test_user).first().favorite_categories.all()
        self.assertEqual(list(test_favourite), self.my_favourite)


