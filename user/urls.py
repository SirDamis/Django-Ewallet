from unicodedata import name
from django.urls import path

from .views import (
    HomeView, 
    RegisterView,
    AccountNotVerifiedView, 
    ActivateAccount
)
from django.conf.urls.static import static
from django.contrib.auth import views

from .forms import EmailValidationOnForgotPassword

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),

    path("login/", views.LoginView.as_view(redirect_authenticated_user=True, template_name = 'html/auth/login.html'), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "password_change/", views.PasswordChangeView.as_view(), name="password_change"
    ),
    path(
        "password_change/done/",
        views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("password_reset/", views.PasswordResetView.as_view(
        form_class=EmailValidationOnForgotPassword,
        template_name='html/auth/password_reset.html', email_template_name='emails/password_reset_link.html'
    ), name="password_reset"),
    path(
        "password_reset/done/",
        views.PasswordResetDoneView.as_view(
            template_name='html/auth/password_reset_done.html',
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(
            template_name='html/auth/password_reset_confirm.html', 
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(
            template_name='html/auth/password_reset_confirm_done.html'
        ),
        name="password_reset_complete",
    ),
    path(
        "account/not-verified/",
        AccountNotVerifiedView.as_view(),
        name="account_not_verified",
    ),

    path(
        'activate/<uidb64>/<token>/', 
        ActivateAccount.as_view(), 
        name='activate'
    ),
]