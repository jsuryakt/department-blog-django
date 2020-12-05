from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Category, Post
from account.models import MyUser
# from django.views import View
from django.views.generic import FormView, ListView, DetailView, CreateView, UpdateView, DeleteView
from blog.forms import ContactForm, PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

# Create your views here.
class SearchView(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "blog/search.html"

    def get_queryset(self):
        query = self.request.GET['query']
        title_queryset = Post.objects.filter(status="P", title__icontains=query)
        content_queryset = Post.objects.filter(status="P", content__icontains=query)
        queryset = title_queryset.union(content_queryset)
        return queryset

class CategoryView(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "blog/category.html"
    queryset = Post.objects.filter(status="P")

    def get_context_data(self):
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        return context
    
    def get_queryset(self):
        category = Category.objects.get(slug = self.request.resolver_match.kwargs.get('slug'))
        queryset = Post.objects.filter(category=category)
        return queryset
    
class ContactView(FormView):
    form_class = ContactForm
    success_url = reverse_lazy("contact-us")
    template_name = "blog/contact_us.html"

class PostListView(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "blog/index.html"
    queryset = Post.objects.filter(status="P")

    def get_context_data(self):
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        return context

class PostDetailView(LoginRequiredMixin, DetailView):
    login_url = "/accounts/login"
    model = Post
    context_object_name = "post"
    template_name = "blog/post_detail.html"
    queryset = Post.objects.filter(status="P")

class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = "/accounts/login"
    permission_required = "blog.add_post"
    form_class = PostForm
    template_name = "blog/post_create_update.html"
    # success_url = "/blogs"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = MyUser.objects.get(username= self.request.user)
        kwargs.update({'initial':{'author': user}})
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = "/accounts/login"
    permission_required = "blog.change_post"
    model = Post
    form_class = PostForm
    template_name = "blog/post_create_update.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = MyUser.objects.get(username= self.request.user)
        kwargs.update({'initial':{'author': user}})
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self, *args, **kwargs):
        current_user = self.request.user
        post_obj = Post.objects.get(slug=self.kwargs.get('slug'))
        post_user = post_obj.author
        if current_user == post_user:
            return True
        else:
            return False

class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    login_url = "/accounts/login"
    permission_required = "blog.delete_post"
    model = Post
    success_url = reverse_lazy('my-posts')
    template_name = "blog/post_delete.html"

    def test_func(self, *args, **kwargs):
        current_user = self.request.user
        post_obj = Post.objects.get(slug=self.kwargs.get('slug'))
        post_user = post_obj.author
        if current_user == post_user:
            return True
        else:
            return False