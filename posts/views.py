# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from posts.forms import PostForm, CategoryForm, CommentForm
from django.shortcuts import render
from posts.models import Post, Comment, Category


def new_category(request):
    current_user = request.user
    if not current_user.is_authenticated:
        return HttpResponseNotAllowed(['GET', 'POST'])
    if request.method == 'POST':
        category_form = CategoryForm(request.POST, request.FILES)
        if category_form.is_valid():
            category = category_form.save(commit=False)
            category.owner = current_user
            category.save()
            return HttpResponseRedirect('/')
    else:
        category_form = CategoryForm()
    return render(request, "categories/new_category.html", {'form': category_form})


def search_category(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
        # TODO: sortowanie po popularności
        categories = Category.objects.filter(category_name__contains=search_text).order_by('category_name')
    else:
        categories = Category.objects.all()
    return render(request, "categories/ajax_search.html", {'categories': categories})


def new_post(request):
    current_user = request.user
    if not current_user.is_authenticated:
        return HttpResponseNotAllowed(['GET', 'POST'])
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = current_user
            post.save()
            return HttpResponseRedirect('/')
    else:
        post_form = PostForm()
    return render(request, "posts/new_post.html", {'form': post_form})


def new_comment(request, post_id, comment_id=None):
    current_user = request.user
    if not current_user.is_authenticated:
        return HttpResponseNotAllowed(['GET', 'POST'])
    if request.method == 'POST':
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = current_user
            comment.post = Post.objects.filter(id=post_id)[0]
            comment.parent = None if comment_id is None else Comment.objects.filter(id=comment_id)[0]
            comment.save()
            return HttpResponseRedirect('/')
    else:
        comment_form = CommentForm()
    return render(request, "comments/new_comment.html", {'form': comment_form})


def show_comments(request, post_id, comment_id=None):
    comments = Comment.objects.filter(post=post_id, parent=comment_id).order_by('-publication_date')
    for comment in comments:
        comment.child_number = count_comments(post_id, comment)
    context = {'comments': comments}
    return render(request, "comments/comments.html", context)


def count_comments(post, comment=None):
    if comment is None:
        return Comment.objects.filter(post=post).count()
    else:
        count = 0
        comments = Comment.objects.filter(post=post, parent=comment)
        count += comments.count()
        for sub_comment in comments:
            count += count_comments(post, sub_comment)
        return count



