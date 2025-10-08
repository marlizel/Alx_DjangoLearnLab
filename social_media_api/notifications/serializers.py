from rest_framework import serializers
from .models import Notification
from django.contrib.contenttypes.models import ContentType


class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField()
    target = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ('id', 'recipient', 'actor', 'verb', 'target', 'unread', 'timestamp')
        read_only_fields = ('id', 'recipient', 'actor', 'verb', 'target', 'timestamp')

    def get_target(self, obj):
        if obj.target is None:
            return None
        ct = ContentType.objects.get_for_id(obj.target_content_type_id)
        return {
            'object_id': obj.target_object_id,
            'model': ct.model,
            'repr': str(obj.target)
        }
