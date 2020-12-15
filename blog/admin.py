from django.contrib import admin
from blog.models import Category, Post
# from blog.forms import ContactForm
# Register your models here.
admin.site.register(Category)
admin.site.register(Post)
# admin.site.register(Contact)