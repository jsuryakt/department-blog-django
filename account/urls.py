from django.urls import path, include
from account.views import UserCreateView, ProfileView, ProfileUpdateView, AuthorRequestView, MyPostsView
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView

urlpatterns = [
    path('signup', UserCreateView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name="account/login.html"), name='login'),

    path('u/<slug:slug>', ProfileView.as_view(), name="profile-view"),
    path('u/<slug:slug>/update', ProfileUpdateView.as_view(), name="profile-update"),

    path('author-request', AuthorRequestView.as_view(), name="author-request"),
    path('my-posts', MyPostsView.as_view(), name="my-posts"),

    path('password-reset/', PasswordResetView.as_view(template_name="account/password_reset.html", email_template_name="account/password_reset_email.html"), name='password-reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name="account/password_reset_done.html"), name='password-reset-done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="account/password_reset_confirm.html"), name='password-reset-confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name="account/password_reset_complete.html"), name='password-reset-complete'),

    path('password-change/', PasswordChangeView.as_view(template_name="account/password_change.html"), name='password-change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name="account/password_change_done.html"), name='password-change-done'),

    path('', include('django.contrib.auth.urls')),
]