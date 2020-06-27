from milk.models import Post
from django.contrib import admin
from django.contrib.auth import get_user_model


User = get_user_model()

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    ordering = ['-created_at']
    list_display = ['short_id', 'title', 'published', 'created_at']

