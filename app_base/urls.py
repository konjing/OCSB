""" app_base urls """
from django.urls import path
from app_base.views import login_view, logout_view, home_view

urlpatterns = [
    path('home/', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
