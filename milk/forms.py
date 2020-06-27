from milk.models import Post, Image, Page
from django import forms

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']
    
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'path', 'body']