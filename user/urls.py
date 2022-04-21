from django.urls import path

from .views import (
    HomeView,
    RegisterView
)

urlpatterns = [
    # path('/login', ),


    path('', HomeView.as_view(), name='homepage'),
]
