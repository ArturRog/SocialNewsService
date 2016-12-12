from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.


@login_required()
def profile(request):
    current_user = request.user

    return render(request, "profile/profile.html", {'user': current_user})

