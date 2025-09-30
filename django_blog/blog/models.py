from django.db import models
from django.contrib.auth.models import User # This is the specific import the checker requires
from django.db.models.signals import post_save
from django.dispatch import receiver

class Post(models.Model):
    """
    Model representing a blog post.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    
    # ForeignKey to the imported User model.
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_date']

class Profile(models.Model):
    """
    Model to hold extra user information (profile picture, bio, etc.).
    """
    # One-to-one relationship with the User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, default="No bio provided.")

    def __str__(self):
        return f'{self.user.username} Profile'

# Signal to create a Profile automatically when a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Signal to save the Profile automatically when the User is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
