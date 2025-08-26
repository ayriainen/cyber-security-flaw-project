from django.contrib import admin
from .models import UserProfile, Note

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_premium', 'note_count']
    list_filter = ['is_premium']
    search_fields = ['user__username']

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'created_at', 'is_public', 'is_shared']
    list_filter = ['is_public', 'is_shared', 'created_at']
    search_fields = ['title', 'owner__username']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['shared_with']
