# -*- coding: utf-8 -*-

from django.contrib import admin

# Register your models here.

from .models import Post, Comment, Report
from category.models import Category

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Report)

# Ewentualnie zeby byly tylko te posty, do ktorych mamy dostep

# class CategoryAdmin(admin.ModelAdmin):
#     def queryset(self, request):
#         qs = super(admin.ModelAdmin, self).queryset(request)
#
#         if request.user.is_superuser:
#             return qs
#
#         user_qs = Post.objects.filter(category=request.user.id)
#         return qs.filter(author__in=user_qs)
