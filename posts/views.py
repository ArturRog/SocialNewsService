from django.http import HttpResponseRedirect
from django.http import HttpResponse
from posts.forms import PostForm
from django.shortcuts import render,redirect


# Create your views here.
from posts.models import Post, Comment


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


def show_comments(request, post_id, comment_id=None):
    # post = Post.objects.filter(id=post_id)
    # comment = None if comment_id is None else Comment.objects.filter(id=comment_id)
    comments = Comment.objects.filter(post=post_id, parent=comment_id).order_by('-publication_date')
    context = {'comments': comments}
    return render(request, "comments/comments.html", context)

