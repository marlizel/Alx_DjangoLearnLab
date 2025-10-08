# notifications/utils.py
from django.contrib.contenttypes.models import ContentType
from .models import Notification

def create_notification(recipient, actor, verb, target=None):
    """
    Create a Notification record in a uniform way.
    `target` can be any model instance (Post, Comment, User, etc).
    """
    target_content_type = None
    target_object_id = None

    if target is not None:
        target_content_type = ContentType.objects.get_for_model(target)
        target_object_id = getattr(target, "id", None)

    return Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        target_content_type=target_content_type,
        target_object_id=target_object_id
    )
