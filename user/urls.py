from unicodedata import name
from django.urls import path

from .views import (
    HomeView,

    ForgotPasswordView,
    RegisterView,
    # LoginView,
    # LogoutView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    
    # path('login/', LoginView.as_view(), name='login'),
    # path('/logout', ),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password' ),


    path('', HomeView.as_view(), name='homepage'),
]
