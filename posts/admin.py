# -*- coding: utf-8 -*-

from django.contrib import admin

# Register your models here.

from .models import Post, Comment, Report

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Report)

