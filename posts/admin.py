# -*- coding: utf-8 -*-

from django.contrib import admin

# Register your models here.

from .models import Post, Comment, ReportMessages, Report

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Report)
admin.site.register(ReportMessages)

