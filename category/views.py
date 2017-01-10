from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from .forms import CategoryForm
from .models import Category
from django.contrib.auth.models import Permission
# Create your views here.


def new_category(request):
    current_user = request.user
    if not current_user.is_authenticated:
        return HttpResponseNotAllowed(['GET', 'POST'])
    if request.method == 'POST':
        category_form = CategoryForm(request.POST, request.FILES)
        if category_form.is_valid():
            category = category_form.save(commit=False)
            category.owner = current_user

            current_user.is_staff = True
            permission1 = Permission.objects.get(name='Can add post')
            permission2 = Permission.objects.get(name='Can change post')
            permission3 = Permission.objects.get(name='Can delete post')
            current_user.user_permissions.add(permission1)
            current_user.user_permissions.add(permission2)
            current_user.user_permissions.add(permission3)
            current_user.save()
            category.save()
            return HttpResponseRedirect('/')
    else:
        category_form = CategoryForm()
    return render(request, "category/new_category.html", {'form': category_form})


def search_category(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
        categories = Category.objects.filter(category_name__contains=search_text).order_by('category_name')
    else:
        categories = Category.objects.all()
    return render(request, "category/ajax_search.html", {'categories': categories})
