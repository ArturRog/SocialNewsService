# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from posts.forms import PostForm, CommentForm
from posts.models import Post, Comment, Report, Report_Comment


@login_required
def new_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect('/')
    else:
        post_form = PostForm()
    return render(request, "posts/new_post.html", {'form': post_form})


@login_required
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if post.author != request.user:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            edited_post = post_form.save(commit=False)
            post.title = edited_post.title
            post.body = edited_post.body
            post.picture = edited_post.picture
            post.original_url = edited_post.original_url
            post.category = edited_post.category
            post.is_modified = True
            post.save()
            return HttpResponseRedirect('/')
    else:
        post_form = PostForm(instance=post)
    return render(request, "posts/new_post.html", {'form': post_form})


@login_required
def new_comment(request, post_id, comment_id=None):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = Post.objects.filter(id=post_id)[0]
            comment.parent = None if comment_id is None else Comment.objects.filter(id=comment_id)[0]
            comment.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))
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


@login_required
def make_report(request, post_id, message):
    report = Report()
    report.post = Post.objects.get(id=post_id)
    report.message = MESSAGES[message]
    report.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def make_report_comment(request, comment_id, message):
    report = Report_Comment()
    report.comment = Comment.objects.get(id=comment_id)
    report.message = MESSAGES[message]
    report.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def show_reports(request):
    reports = Report.objects.all()
    context = {'reports': reports}
    return render(request, "reports/reports.html", context)


@login_required
def show_reports_comment(request):
    reports = Report_Comment.objects.all()
    context = {'reports': reports}
    return render(request, "reports/reports_comment.html", context)
