from django import forms
from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        # 用到哪個model
        model = Post
        # 要show出來的欄位(?)
        fields = ('title', 'text',)
