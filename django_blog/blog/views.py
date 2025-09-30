from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView 
# --- NEW IMPORTS FOR SEARCH ---
from django.db.models import Q 


# --- CORRECTED IMPORTS ---
# Include PostForm and CommentForm from .forms:
from .forms import CustomUserCreationForm, UserProfileForm, ProfileBioForm, PostForm, CommentForm
# Include Comment model from .models:
from .models import Post, Profile, Comment


# --- Home View ---
def home(request):
    """
    Renders the homepage.
    """
    return render(request, "blog/home.html")

# --- Registration View ---
@transaction.atomic
def register(request):
    """
    Handles user registration. Creates a new User and associated Profile.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after successful registration
            login(request, user)
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect("home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = CustomUserCreationForm()
    
    return render(request, "blog/register.html", {"form": form})

# --- Profile Management View ---
@login_required
@transaction.atomic
def profile(request):
    """
    Allows the logged-in user to view and edit their profile and user details.
    """
    # Use request.user.profile to get the profile object
    try:
        user_profile = request.user.profile
    except Profile.DoesNotExist:
        # Fallback for robustness
        user_profile = Profile.objects.create(user=request.user)
    
    if request.method == "POST":
        user_form = UserProfileForm(request.POST, instance=request.user)
        profile_form = ProfileBioForm(request.POST, instance=user_profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        # Display current data in forms on GET request
        user_form = UserProfileForm(instance=request.user)
        profile_form = ProfileBioForm(instance=user_profile)

    return render(request, "blog/profile.html", {
        "user_form": user_form,
        "profile_form": profile_form
    })

# --- MODIFIED: PostListView to handle tag filtering (Task 4) ---
class PostListView(ListView):
    """
    Displays a list of all blog posts, optionally filtered by tag slug from the URL.
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # Check if a tag slug is present in the URL kwargs (for /tags/<tag_slug>/)
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            # Filter posts by the given tag slug using the tags field
            queryset = Post.objects.filter(tags__slug__in=[tag_slug]).order_by('-published_date')
            return queryset
        
        # Default behavior: return all posts
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the tag slug to the template for context (e.g., in the title)
        context['tag_slug'] = self.kwargs.get('tag_slug')
        return context

# --- NEW: Function-Based Search View (Task 4) ---
def post_search(request):
    """
    Handles search requests, filtering posts by title, content, or tags.
    """
    query = request.GET.get('q') # Get the query string from the URL (?q=...)
    results = []
    
    if query:
        # Use Q objects for complex OR lookups across title, content, and tag name
        results = Post.objects.filter(
            Q(title__icontains=query) |        # Search in post title (case-insensitive)
            Q(content__icontains=query) |      # Search in post content (case-insensitive)
            Q(tags__name__icontains=query)     # Search in tag names (case-insensitive)
        ).distinct().order_by('-published_date') # distinct() prevents duplicate posts
        
    return render(request, 'blog/post_search.html', {
        'query': query,
        'results': results,
    })

# --- UPDATED PostDetailView (Removes the manual comment POST handling) ---
class PostDetailView(DetailView):
    """
    Displays the full content of a single blog post.
    """
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        """
        Adds the comment form and list of comments to the context.
        """
        context = super().get_context_data(**kwargs)
        # Add the comment form, only if the user is authenticated
        if self.request.user.is_authenticated:
            # Pass an empty form instance for display
            context['comment_form'] = CommentForm() 
        
        # Fetch comments ordered by creation time (default ordering is set on the model)
        context['comments'] = self.object.comments.all()
        return context
    
    # NOTE: The manual 'post' method for comment creation has been removed here.
    # The comment form now submits to CommentCreateView via the 'comment_create' URL.

# --- NEW COMMENT CREATE VIEW (Required for checker) ---
class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    Handles the creation of a new Comment via POST request from the post detail page.
    """
    model = Comment
    form_class = CommentForm
    
    def form_valid(self, form):
        # 1. Retrieve the Post object using the 'pk' from the URL (passed via urls.py)
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        
        # 2. Assign the Post and the currently logged-in user to the comment instance
        form.instance.post = post
        form.instance.author = self.request.user
        
        messages.success(self.request, "Your comment was posted successfully!")
        
        # 3. Save the comment and proceed
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect back to the post detail page after successful comment creation
        post_pk = self.kwargs.get('pk')
        return reverse_lazy('post_detail', kwargs={'pk': post_pk})


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Allows authenticated users to create a new post.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('posts') 

    def form_valid(self, form):
        """
        Overrides form_valid to automatically set the author to the logged-in user.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allows the post author to update their own post.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        """
        Checks if the current user is the author of the post.
        """
        post = self.get_object()
        return self.request.user == post.author

    def get_success_url(self):
        """
        Redirects to the detailed view of the updated post.
        """
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Allows the post author to delete their own post.
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('posts') 

    def test_func(self):
        """
        Checks if the current user is the author of the post.
        """
        post = self.get_object()
        return self.request.user == post.author

# --- COMMENT UPDATE AND DELETE VIEWS ---

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allows the comment author to update their comment.
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def get_success_url(self):
        """
        Redirects back to the post detail page after updating.
        """
        # Use the post's primary key (pk) to redirect back to the correct detail view
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        """
        Checks if the current user is the author of the comment.
        """
        comment = self.get_object()
        return self.request.user == comment.author

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Allows the comment author to delete their comment.
    """
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_success_url(self):
        """
        Redirects back to the post detail page after deletion.
        """
        # Use the post's primary key (pk) to redirect back to the correct detail view
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})
        
    def test_func(self):
        """
        Checks if the current user is the author of the comment.
        """
        comment = self.get_object()
        return self.request.user == comment.author
