from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('reset/<uidb64>/<token>', views.passwordResetConfirm, name='activate'),
    path("activate/<uidb64>/<token>", views.activate, name="activate"),
    path("profile/", views.profile, name="profile"),
    path("change_password/", views.change_password, name="change_password"),
    path("password_reset/", views.password_reset, name="password_reset"),
    path('reset/<uidb64>/<token>', views.passwordResetConfirm, name='reset'),
    path('login/', auth_views.LoginView.as_view(template_name="registration/login.html", redirect_authenticated_user=True), name='login'),
]