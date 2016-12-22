# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.
from posts.models import Post
from category.models import Category
from user_profile.models import UserProfile
from .forms import RegisterForm
from django.shortcuts import get_object_or_404
from posts.views import count_comments, show_posts
from datetime import datetime, timedelta
from django.template.loader import render_to_string


def post_filter(posts, filtr):
    if filtr == 'dzien':
        posts = posts.filter(publication_date__gte=datetime.now() - timedelta(days=1)).order_by('-votes')
    elif filtr == 'tydzien':
        posts = posts.filter(publication_date__gte=datetime.now() - timedelta(days=7)).order_by('-votes')
    elif filtr == 'miesiac':
        posts = posts.filter(publication_date__gte=datetime.now() - timedelta(days=30)).order_by('-votes')
    elif filtr == 'najnowsze':
        posts = posts.order_by('-publication_date')

    return posts


def home(request, filtr=None):
    # posts_response = show_posts(request)
    # context = {'posts_response': posts_response}
    posts = Post.objects.all()

    if filtr:
        posts = post_filter(posts, filtr)
        request.path = "/"

    context = {'posts': posts}
    return render(request, "main/home.html", context)


@login_required()
def upvote_news(request, pk):
    post = get_object_or_404(Post, id=pk)
    user = post.author
    user_profile = UserProfile.objects.get(user=user)
    user_profile.reputation += 1
    user_profile.save()
    post.votes += 1
    post.save()
    return redirect("/")


@login_required()
def downvote_news(request, pk):
    post = get_object_or_404(Post, id=pk)
    user = post.author
    user_profile = UserProfile.objects.get(user=user)
    user_profile.reputation -= 1
    user_profile.save()
    post.votes -= 1
    post.save()
    return redirect("/")


def category_filter(request, pk, filtr=None):
    posts = Post.objects.filter(category__id=pk)
    category = Category.objects.get(id=pk)
    # posts_response = show_posts(request, 1, category=None)
    # context = {'posts_response': posts_response, 'category': category}

    if filtr:
        posts = post_filter(posts, filtr)
        request.path = "/category/" + pk + '/'
    context = {'posts': posts, 'category': category}

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
        form = RegisterForm
    return render(request, "main/register.html", {'form': form})
