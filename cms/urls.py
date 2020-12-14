from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from blog.views import PostListView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('blogs/', include('blog.urls')),
    path('accounts/', include('account.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('', PostListView.as_view(), name="index")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)