# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.http import HttpResponse
from posts.forms import PostForm
from django.shortcuts import render,redirect

# Create your views here.


def new_post(request):
    current_user = request.user
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = current_user
            post.save()
            # return HttpResponseRedirect(redirect_to="home.html")
    else:
        post_form = PostForm()
    return render(request, "posts/new_post.html", {'form': post_form})
