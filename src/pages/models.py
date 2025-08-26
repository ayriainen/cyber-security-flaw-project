from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_premium = models.BooleanField(default=False)
    note_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} ({'Premium' if self.is_premium else 'Basic'})"

class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)

    shared_with = models.ManyToManyField(User, blank=True, related_name='shared_notes')
    is_shared = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} by {self.owner.username}"
