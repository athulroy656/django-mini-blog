from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import User, BlogPost, Comment
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q

# Create your views here.

def home(request):
    # Get latest 3 blog posts
    latest_posts = BlogPost.objects.all()[:3]
    
    # Get active bloggers (users who have posted in the last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    active_bloggers = User.objects.filter(
        blog_posts__created_at__gte=thirty_days_ago
    ).distinct().order_by('-blog_posts__created_at')[:5]
    
    return render(request, 'index.html', {
        'latest_posts': latest_posts,
        'active_bloggers': active_bloggers
    })

def about(request):
    return render(request, 'about.html')

def search_posts(request):
    query = request.GET.get('q', '')
    if query:
        posts = BlogPost.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        ).order_by('-created_at')
    else:
        posts = []
    
    context = {
        'posts': posts,
        'query': query,
    }
    return render(request, 'search_results.html', context)

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        full_name = request.POST.get('full_name', username)  # Use username as default if full_name not provided
        
        # Validation
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
        
        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long')
            return redirect('register')
        
        # Create user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                full_name=full_name
            )
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'An error occurred during registration: {str(e)}')
            return redirect('register')
    
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Set session variable to show welcome toast
            request.session['show_welcome_toast'] = True
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')

@require_POST
def clear_welcome_toast(request):
    if 'show_welcome_toast' in request.session:
        del request.session['show_welcome_toast']
    return JsonResponse({'status': 'success'})

def blog_list(request):
    posts = BlogPost.objects.all()
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, 'blog_list.html', {'posts': posts})

def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    comments = post.comments.all()
    context = {
        'post': post,
        'comments': comments,
        'total_likes': post.total_likes(),
    }
    return render(request, 'blog_detail.html', context)

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Comment.objects.create(
                content=content,
                author=request.user,
                post=post
            )
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Comment cannot be empty.')
    return redirect('blog_detail', post_id=post_id)

def author_detail(request, author_id):
    author = get_object_or_404(User, id=author_id)
    posts = BlogPost.objects.filter(author=author)
    return render(request, 'author_detail.html', {'author': author, 'posts': posts})

def blogger_detail(request, author_id):
    author = get_object_or_404(User, id=author_id)
    posts = BlogPost.objects.filter(author=author).order_by('-created_at')
    return render(request, 'blogger_detail.html', {
        'author': author,
        'posts': posts
    })

def blogger_list(request):
    # Get all users who have published at least one blog post
    bloggers = User.objects.filter(blog_posts__isnull=False).distinct().order_by('username')
    return render(request, 'blogger_list.html', {'bloggers': bloggers})

@login_required
@require_POST
def like_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    
    if post.is_liked_by(request.user):
        # User has already liked the post, so unlike it
        post.unlike(request.user)
        liked = False
    else:
        # User hasn't liked the post yet, so like it
        post.like(request.user)
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'disliked': post.is_disliked_by(request.user),
        'total_likes': post.total_likes()
    })

@login_required
@require_POST
def dislike_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    
    if post.is_disliked_by(request.user):
        # User has already disliked the post, so remove dislike
        post.undislike(request.user)
        disliked = False
    else:
        # User hasn't disliked the post yet, so dislike it
        post.dislike(request.user)
        disliked = True
    
    return JsonResponse({
        'liked': post.is_liked_by(request.user),
        'disliked': disliked,
        'total_likes': post.total_likes()
    })

@login_required
def saved_posts(request):
    saved_posts = request.user.bookmarks.all().order_by('-created_at')
    return render(request, 'saved_posts.html', {'posts': saved_posts})

@login_required
@require_POST
def toggle_bookmark(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    
    if post in request.user.bookmarks.all():
        request.user.bookmarks.remove(post)
        bookmarked = False
    else:
        request.user.bookmarks.add(post)
        bookmarked = True
    
    return JsonResponse({
        'bookmarked': bookmarked
    })

@login_required
@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check if the user is the author of the comment
    if request.user == comment.author:
        comment.delete()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'You are not authorized to delete this comment'}, status=403)
