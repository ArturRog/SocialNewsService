from django.forms import ModelForm
from posts.models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'picture', 'original_url', "category"]

