from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().select_related('author').prefetch_related('comments')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().select_related('author', 'post')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

# import PostSerializer and Post model are already present above in the file;
# if not, ensure these imports exist at the top:
# from .models import Post
# from .serializers import PostSerializer

class FeedView(ListAPIView):
    """
    Feed for the authenticated user: posts by users they follow,
    ordered by most recent first.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination  # uses the same pagination you already set

    def get_queryset(self):
        user = self.request.user
        # user.following returns the users this user follows (from related_name='following')
        following_users = user.following.all()
        return Post.objects.filter(author__in=following_users).select_related('author').prefetch_related('comments').order_by('-created_at')
