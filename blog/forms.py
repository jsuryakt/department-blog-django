from django import forms
import re
from django.forms import ModelForm
from blog.models import Post, Contact, Comment
from tinymce.widgets import TinyMCE

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone_number', 'message']

class PostForm(ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    author = forms.CharField(disabled=True)

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]