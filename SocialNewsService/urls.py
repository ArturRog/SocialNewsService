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
from main.views import home,register,upvote_news,downvote_news, category_filter
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from posts.views import new_post


urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^$', home, name='home'),
                  # url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
                  url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
                  url(r'^logout/$', auth_views.logout, {'next_page': 'home'}, name='logout'),
                  url(r'^register/$', register, name='register'),
                  url(r'^new_post/$', new_post, name='new_post'),
                  url(r'^upvote_news/(?P<pk>\d+)/$', upvote_news, name='upvote_news'),
                  url(r'^downvote_news/(?P<pk>\d+)/$', downvote_news, name='downvote_news'),
                  url(r'^category/(?P<pk>\d+)/$', category_filter, name='category_filter')


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns += [
#     url(r'^login/$', views.login, {'template_name': 'login.html'}, name='login'),
#     url(r'^logout/$', views.logout, {'next_page': 'home'}, name='logout')
#
# ]
