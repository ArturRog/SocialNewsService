from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
from posts.models import Post


def home(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, "main/home.html", context)
