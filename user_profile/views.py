from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from posts.models import Category, Post
from user_profile.models import UserProfile


# Create your views here.

def menu_context(request):
    current_user = request.user
    categories = Category.objects.filter(owner=current_user)
    user_profile = UserProfile.objects.get(user=current_user)
    fav_categories = user_profile.favorite_categories.all()
    context = {'current_user': current_user, 'categories': categories, 'fav_categories': fav_categories}
    return context


@login_required()
def profile(request):
    return render(request, "userprofile.html", menu_context(request))


# wyswietla posty z naszej kategorii
@login_required()
def my_categories(request, pk):
    context = menu_context(request)

    posts = Post.objects.filter(category__id=pk).order_by('-publication_date')
    context.update({'posts': posts})
    return render(request, "profile/profile.html", context)


@login_required()
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
