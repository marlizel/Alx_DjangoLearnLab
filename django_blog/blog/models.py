from django.db import models
from django.contrib.auth import get_user_model

# Get the custom user model (which defaults to the built-in Django User model)
User = get_user_model()

class Post(models.Model):
    """
    Model representing a blog post, fulfilling the requirements of the task.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    
    # ForeignKey to the User model, linking a post to its author.
    # on_delete=models.CASCADE ensures all posts are deleted if the author is deleted.
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns the title of the post for easy readability (e.g., in the admin).
        """
        return self.title

    class Meta:
        # Orders posts by publication date, newest first
        ordering = ['-published_date']
