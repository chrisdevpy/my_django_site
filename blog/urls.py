from django.urls import path
from . import views

urlpatterns = [
    # '' means empty, if you go to 127.0.0.1:8000 go to views.py/post_list()
    path('', views.post_list, name='post_list'),
]