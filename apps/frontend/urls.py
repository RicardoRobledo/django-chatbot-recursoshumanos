from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
