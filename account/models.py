from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.contrib.auth.models import Group
from django.urls import reverse

# Create your models here.
class MyUser(AbstractUser):
    email = models.EmailField(unique=True)
    slug = models.CharField(max_length=60, unique=True, blank=True)
    bio = models.CharField(max_length=500, blank=True)
    profile_image = models.ImageField(upload_to="account/profile_pic", default="profile-default.jpg", blank=True)
    is_author = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super().save()

    def get_absolute_url(self, *args, **kwargs):
        return reverse('profile-update', kwargs={'slug':self.slug})

class Request(models.Model):
    statuses = [
        ('T', 'True'),
        ('F', 'False')
    ]
    sender = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    message = models.TextField()
    is_approved = models.CharField(max_length=1, choices=statuses, default='F')

    def __str__(self):
        return "Author Request by {}".format(self.sender.username)

    def save(self, *args, **kwargs):
        if self.is_approved == 'T':
            author_group = Group.objects.get(name = "Author")
            self.sender.groups.add(author_group)
            self.sender.is_author = True
            self.sender.save()
        super().save()

    def get_absolute_url(self, *args, **kwargs):
        slug = self.sender.slug
        return reverse('profile-update', kwargs={'slug':slug})