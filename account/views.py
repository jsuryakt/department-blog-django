from django.shortcuts import render
from account.models import MyUser
from django.views.generic import ListView, DetailView, CreateView, UpdateView
# from django.contrib.auth.forms import UserCreationForm
from account.forms import SignUpForm, ProfileUpdateForm, AuthorRequestForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

# Create your views here.
class UserCreateView(CreateView):
    form_class = SignUpForm
    template_name = "account/signup.html"
    success_url = reverse_lazy("login")

class ProfileView(DetailView):
    model = MyUser
    content_object_name = "user"
    template_name = "account/profile.html"

class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = "/accounts/login"
    model = MyUser
    form_class = ProfileUpdateForm
    template_name = "account/profile_update.html"

    def test_func(self, *args, **kwargs):
        current_user = self.request.user
        profile_obj = MyUser.objects.get(slug=self.kwargs.get('slug'))
        if current_user == profile_obj:
            return True
        else:
            return False

class AuthorRequestView(LoginRequiredMixin, CreateView):
    login_url = "/accounts/login"
    form_class = AuthorRequestForm
    template_name = "account/author_request.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = MyUser.objects.get(username= self.request.user)
        kwargs.update({'initial':{'sender': user}})
        return kwargs

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)

class MyPostsView(LoginRequiredMixin, ListView):
    login_url = "/accounts/login"
    model = MyUser
    context_object_name = "user"
    template_name = "account/my_posts.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        user = MyUser.objects.get(username = self.request.user)
        context['posts'] = user.post_set.all()
        return context