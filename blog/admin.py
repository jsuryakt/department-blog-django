from django.contrib import admin
from blog.models import Category, Post, Contact, Comment
# from blog.forms import ContactForm
# Register your models here.
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Contact)
admin.site.register(Comment)