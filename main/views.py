from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
from posts.models import Post
from .forms import RegisterForm


def home(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, "main/home.html", context)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm
    return render(request, "main/register.html", {'form': form})
