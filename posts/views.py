# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from posts.forms import PostForm, CommentForm
from django.shortcuts import render, redirect
from posts.models import Post, Comment, Category, Report
from django.contrib.auth.models import User


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


def show_posts(request, page_number=None, category=None):
    posts = Post.objects.all()
    for post in posts:
        post.comments_number = count_comments(post)
    context = {'posts': posts}
    return render(request, "posts/posts.html", context)


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
    context = {
        'form': comment_form,
        'post': Post.objects.filter(id=post_id).first(),
        'comment': Comment.objects.filter(id=comment_id).first()
    }
    return render(request, "comments/new_comment.html", context)


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


MESSAGES = {
    '1': 'Spam',
    '2': 'Obrazliwe tresci',
    '3': 'Nieprawdziwa informacja',
    '4': 'Propagowanie przemocy'
}


def make_report(request, post_id, message):
    report = Report()
    report.post = Post.objects.get(id=post_id)
    report.message = MESSAGES[message]
    report.save()
    return redirect("/")


def show_reports(request):
    reports = Report.objects.all()
    context = {'reports': reports}
    return render(request, "reports/reports.html", context)
