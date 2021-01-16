from django.db import models
from account.models import MyUser

from django.utils.text import slugify
from tinymce import models as tinymce_models
from bs4 import BeautifulSoup
from django.urls import reverse
from django.core.validators import RegexValidator

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    slug = models.CharField(max_length=60, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save()

    def get_absolute_url(self, *args, **kwargs):
        return reverse('category', kwargs={'slug':self.slug})

class Post(models.Model):
    statuses = [
        ('D', 'Draft'),
        ('P', 'Publish')
    ]
    title = models.CharField(max_length=120, unique=True)
    slug = models.CharField(max_length=60, unique=True, blank=True)
    # content = models.TextField()
    content = tinymce_models.HTMLField()
    status = models.CharField(max_length=1, choices=statuses, default= 'D')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog/post', default="post-default.jpg")
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save()

    def get_absolute_url(self, *args, **kwargs):
        return reverse('post-update', kwargs={'slug':self.slug})

    def html_to_text(self, *args, **kwargs):
        soup = BeautifulSoup(self.content, features="html.parser")
        text = soup.get_text()
        return text

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    content = models.TextField(max_length=460)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {} - ({})".format(self.post.title, self.user.username,self.content)

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_regex = RegexValidator(regex=r'^[6-9][0-9]{9}$', message="Phone number must be a 10 digit valid Indian number without any symbols, character, STD pin!")
    phone_number = models.CharField(validators=[phone_regex], max_length=10, blank=True) # validators should be a list
    message = models.CharField(max_length=500) #widget=forms.Textarea
    REQUIRED_FIELDS = ['email', 'name', 'message']

    def __str__(self):
        return self.message