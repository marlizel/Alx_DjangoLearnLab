from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

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
    try:
        user_profile = request.user.profile
    except Profile.DoesNotExist:
        # Should not happen if signals are working, but here for robustness
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

class PostListView(ListView):
    """
    Displays a list of all blog posts. Accessible to all users.
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

# --- UPDATED for Comment Creation (Task 3) ---
class PostDetailView(DetailView):
    """
    Displays the full content of a single blog post and handles comment creation (POST).
    Accessible to all users.
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
            # Pass an empty form instance for GET request display
            context['comment_form'] = CommentForm() 
        
        # Fetch comments ordered by creation time
        context['comments'] = self.object.comments.all()
        return context

    def post(self, request, *args, **kwargs):
        """
        Handles the submission of a new comment form (POST request).
        """
        # Fetch the Post object that the comment is for
        self.object = self.get_object() 
        
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to post a comment.")
            return redirect('post_detail', pk=self.object.pk)

        comment_form = CommentForm(request.POST)
        
        if comment_form.is_valid():
            # Create comment instance but don't save yet
            comment = comment_form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            messages.success(request, "Your comment was posted successfully!")
            # Redirect back to the post detail page
            return redirect('post_detail', pk=self.object.pk)
        
        # If the form is invalid, re-render the page with errors
        context = self.get_context_data()
        context['comment_form'] = comment_form
        return self.render_to_response(context)


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Allows authenticated users to create a new post.
    Requires LoginRequiredMixin.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('posts') # Redirect to the post list upon success

    def form_valid(self, form):
        """
        Overrides form_valid to automatically set the author to the logged-in user.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allows the post author to update their own post.
    Requires LoginRequiredMixin (authenticated) and UserPassesTestMixin (author check).
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
    Requires LoginRequiredMixin (authenticated) and UserPassesTestMixin (author check).
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('posts') # Redirect to the post list after deletion

    def test_func(self):
        """
        Checks if the current user is the author of the post.
        """
        post = self.get_object()
        return self.request.user == post.author

# --- NEW COMMENT VIEWS (Task 3) ---

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
