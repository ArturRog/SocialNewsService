from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from posts.models import Comment, Post
from category.models import Category
from posts.views import count_comments
from user_profile.models import UserProfile


# Create your views here.

@login_required
def menu_context(request):
    current_user = request.user
    categories = Category.objects.filter(owner=current_user)
    user_profile = UserProfile.objects.get(user=current_user)
    fav_categories = user_profile.favorite_categories.all()
    reputation = user_profile.reputation
    comments = Comment.objects.filter(author=current_user)
    posts = Post.objects.filter(author=current_user)
    for post in posts:
        post.comments_number = count_comments(post)
    context = {'current_user': current_user, 'categories': categories, 'fav_categories': fav_categories,
               'reputation': reputation, 'comments': comments, 'user_profile': user_profile, 'posts': posts}
    return context


@login_required()
def profile(request):
    return render(request, "profile/settings.html", menu_context(request))


# wyswietla posty z naszej kategorii
@login_required()
def my_categories(request, pk):
    context = menu_context(request)
    posts = Post.objects.filter(category__id=pk).order_by('-publication_date')
    for post in posts:
        post.comments_number = count_comments(post)
    context.update({'posts': posts})
    return render(request, "profile/posts.html", context)


@login_required
def my_comments(request):
    return render(request, "profile/comments.html", menu_context(request))


@login_required
def my_settings(request):
    return render(request, "profile/settings.html", menu_context(request))


@login_required
def my_posts(request):
    return render(request, "profile/posts.html", menu_context(request))


@login_required
def add_to_favorites(request, pk):
    current_user = request.user
    current_user_profile = UserProfile.objects.get(user=current_user)
    category = Category.objects.get(id=pk)

    current_favorite_categories = current_user_profile.favorite_categories.all()
    if category not in current_favorite_categories:
        current_user_profile.favorite_categories.add(category)
    else:
        current_user_profile.favorite_categories.remove(category)
    current_user_profile.save()

    return redirect('/category/' + pk)
