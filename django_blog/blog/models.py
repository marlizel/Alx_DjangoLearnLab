from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from taggit.managers import TaggableManager # <-- NEW IMPORT

# --- Blog Post Model (Updated for Tagging) ---
class Post(models.Model):
    """
    Model representing a blog post.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    # It's better practice to use 'created_on' or 'published_date' consistently, 
    # but we maintain 'published_date' as per your original file.
    published_date = models.DateTimeField(auto_now_add=True) 
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # --- TAGGING FIELD ADDED ---
    tags = TaggableManager() 

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_date']

# --- User Profile Model (Existing) ---
class Profile(models.Model):
    """
    Model to hold extra user information (profile picture, bio, etc.).
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, default="No bio provided.")

    def __str__(self):
        return f'{self.user.username} Profile'

# Signal handlers for Profile (Existing)
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

# --- Comment Model (Existing) ---
class Comment(models.Model):
    """
    Model representing a comment on a blog post.
    """
    # Link to the specific post the comment is on
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # Link to the user who wrote the comment
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # The actual text of the comment
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at'] # Order comments chronologically

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
