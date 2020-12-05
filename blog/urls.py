from django.urls import path
from blog.views import SearchView, CategoryView, ContactView, PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('search', SearchView.as_view(), name="search"),
    path('category/<slug:slug>', CategoryView.as_view(), name="category"),
    path('contact-us',ContactView.as_view(), name="contact-us"),

    path('', PostListView.as_view(), name="index"),
    path('posts/<slug:slug>', PostDetailView.as_view(), name="post-detail"),

    path('posts', PostCreateView.as_view(), name="post-create"),
    path('posts/<slug:slug>/update', PostUpdateView.as_view(), name="post-update"),
    path('posts/<slug:slug>/delete', PostDeleteView.as_view(), name="post-delete"),
]