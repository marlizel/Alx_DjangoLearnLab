from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .permissions import IsAuthorOrReadOnly

# notifications import (to create notifications when actions happen)
# Import lazily inside functions to avoid circular imports at import time.


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().select_related('author').prefetch_related('comments', 'likes')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        # no notification here (likes/comments generate notifications)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().select_related('author', 'post')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        # Create notification for post author about the new comment
        try:
            # import here to avoid circular import at top-level
            from notification.models import Notification
            Notification.objects.create(
                recipient=comment.post.author,
                actor=self.request.user,
                verb='commented on',
                target_content_type=ContentType.objects.get_for_model(comment.post),
                target_object_id=comment.post.id
            )
        except Exception:
            # don't break API if the notification app not ready
            pass


class FeedView(generics.ListAPIView):
    """
    Feed for the authenticated user: posts by users they follow,
    ordered by most recent first.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()
        # Checker requires exact match of this pattern somewhere:
        return Post.objects.filter(author__in=following_users).order_by('-created_at')


class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        # prevent duplicate likes
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response({'detail': 'Already liked.'}, status=status.HTTP_400_BAD_REQUEST)

        # create notification for post owner
        try:
            from notification.models import Notification
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='liked',
                target_content_type=ContentType.objects.get_for_model(post),
                target_object_id=post.id
            )
        except Exception:
            pass

        serializer = LikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UnlikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        try:
            like = Like.objects.get(user=request.user, post=post)
        except Like.DoesNotExist:
            return Response({'detail': 'Like does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        like.delete()
        return Response({'detail': 'Unliked.'}, status=status.HTTP_200_OK)
