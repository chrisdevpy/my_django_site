from django.contrib import admin
# The bottom import is importing the class Post from models.py
from .models import Post

# Register your models here.
admin.site.register(Post)