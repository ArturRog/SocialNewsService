# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.timezone import utc

from posts.models import Post, PostVotes
from category.models import Category
from user_profile.models import UserProfile
from .forms import RegisterForm
from django.shortcuts import get_object_or_404
from posts.views import count_comments
from datetime import datetime, timedelta


def post_filter(posts, filtr):
    now = datetime.now().utcnow().replace(tzinfo=utc)
    if filtr == 'dzien':
        posts = posts.filter(publication_date__gte=now - timedelta(days=1)).order_by('-votes')
    elif filtr == 'tydzien':
        posts = posts.filter(publication_date__gte=now - timedelta(days=7)).order_by('-votes')
    elif filtr == 'miesiac':
        posts = posts.filter(publication_date__gte=now - timedelta(days=30)).order_by('-votes')
    elif filtr == 'najnowsze':
        posts = posts.order_by('-publication_date')
    return posts


def home(request, filtr=None):
    posts = Post.objects.all()
    if filtr:
        posts = post_filter(posts, filtr)
        request.path = "/"
    for post in posts:
        post.comments_number = count_comments(post)
    context = {'posts': posts}
    return render(request, "main/home.html", context)


@login_required
def upvote_news(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    voting_user = request.user
    vote = PostVotes.objects.filter(post=post, user=voting_user).first()
    if vote is None:
        vote = PostVotes()
        vote.post = post
        vote.user = voting_user
    author = post.author
    user_profile = UserProfile.objects.get(user=author)
    if vote.vote == 0:
        user_profile.reputation += 1
        post.votes += 1
    elif vote.vote == -1:
        user_profile.reputation += 2
        post.votes += 2
    vote.vote = 1
    vote.save()
    user_profile.save()
    post.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def downvote_news(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    voting_user = request.user
    vote = PostVotes.objects.filter(post=post, user=voting_user).first()
    if vote is None:
        vote = PostVotes()
        vote.post = post
        vote.user = voting_user
    author = post.author
    user_profile = UserProfile.objects.get(user=author)
    if vote.vote == 0:
        user_profile.reputation -= 1
        post.votes -= 1
    elif vote.vote == 1:
        user_profile.reputation -= 2
        post.votes -= 2
    vote.vote = -1
    vote.save()
    user_profile.save()
    post.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))


def category_filter(request, pk, filtr=None):
    posts = Post.objects.filter(category__id=pk)
    category = Category.objects.get(id=pk)
    if filtr:
        posts = post_filter(posts, filtr)
        request.path = "/category/" + pk + '/'
    for post in posts:
        post.comments_number = count_comments(post)
    if request.user.is_authenticated:
        is_favorite = category in UserProfile.objects.filter(user=request.user).first().favorite_categories.all()
    else:
        is_favorite = False
    context = {
        'category': category,
        'posts': posts,
        'is_favorite': is_favorite
    }
    return render(request, "main/home.html", context)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            user_profile = UserProfile()
            user_profile.user = User.objects.get(username=form.data['username'])
            user_profile.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, "main/register.html", {'form': form})
