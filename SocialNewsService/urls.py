"""SocialNewsService URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from main.views import home, register, upvote_news, downvote_news, category_filter
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from user_profile.views import profile, my_categories, add_to_favorites, my_comments, my_settings, my_posts
from posts.views import new_post, show_comments, new_comment, show_posts, make_report, show_reports, edit_post
from category.views import new_category, search_category

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^$', home, name='home'),
                  url(r'^cat-(?P<filtr>\w+)/$', home, name='home'),
                  # url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
                  url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
                  url(r'^logout/$', auth_views.logout, {'next_page': 'home'}, name='logout'),
                  url(r'^register/$', register, name='register'),
                  url(r'^profile/$', profile, name='profile'),
                  url(r'^add_to_favorites/(?P<pk>\d+)/$', add_to_favorites, name='add_to_favorites'),
                  url(r'^my_categories/(?P<pk>\d+)/$', my_categories, name='my_categories'),
                  url(r'^my_comments/$', my_comments, name='my_comments'),
                  url(r'^my_settings/$', my_settings, name='my_settings'),
                  url(r'^my_posts/$', my_posts, name='my_posts'),
                  url(r'^new_post/$', new_post, name='new_post'),
                  url(r'^edit_post/(?P<post_id>\d+)/$', edit_post, name='edit_post'),

                  # url(r'^report/(?P<post_id>\d+)/(?P<message>\d+)/$', make_report, name='make_report'),
                  url(r'^report/(?P<post_id>\d+)/(?P<message>\d+)/$', make_report, name='report'),
                  url(r'^reports/$', show_reports, name='reports'),

                  url(r'^posts/show_posts/$', show_posts, name='show_posts'),
                  url(r'^posts/show_posts/(?P<page_number>[0-9]+)/$', show_posts, name='show_posts'),

                  url(r'^comments/show-comments/(?P<post_id>[0-9]+)/$', show_comments, name='show_comments'),
                  url(r'^comments/show-comments/(?P<post_id>[0-9]+)/(?P<comment_id>[0-9]+)/$', show_comments,
                      name='show_comments'),
                  url(r'^comments/new_comment/(?P<post_id>[0-9]+)/$', new_comment, name='new_comment'),
                  url(r'^comments/new_comment/(?P<post_id>[0-9]+)/(?P<comment_id>[0-9]+)/$', new_comment,
                      name='new_comment'),

                  url(r'^new_category/$', new_category, name='new_category'),
                  url(r'^search_category/$', search_category, name='search_category'),
                  url(r'^upvote_news/(?P<post_id>[0-9]+)/$', upvote_news, name='upvote_news'),
                  url(r'^downvote_news/(?P<post_id>[0-9]+)/$', downvote_news, name='downvote_news'),
                  url(r'^category/(?P<pk>\d+)/$', category_filter, name='category_filter'),
                  url(r'^category/(?P<pk>\d+)/cat-(?P<filtr>\w+)/$', category_filter, name='category_filter'),


              ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns += [
#     url(r'^login/$', views.login, {'template_name': 'login.html'}, name='login'),
#     url(r'^logout/$', views.logout, {'next_page': 'home'}, name='logout')
#
# ]
