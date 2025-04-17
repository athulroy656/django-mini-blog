"""
Script to populate the database with sample data for testing
"""
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
django.setup()

from app.models import User, BlogPost, Comment
from django.utils import timezone
from django.db import transaction

def create_sample_data():
    print("Creating sample data...")
    
    # Check if we already have users
    if User.objects.count() > 0:
        print("Data already exists, skipping...")
        return
    
    # Create admin user if it doesn't exist
    admin_user = User.objects.filter(username='admin').first()
    if not admin_user:
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin',
            full_name='Admin User'
        )
        print("Created admin user")
    
    # Create sample users
    users = []
    for i in range(1, 4):
        user = User.objects.create_user(
            username=f'user{i}',
            email=f'user{i}@example.com',
            password=f'password{i}',
            full_name=f'User {i}'
        )
        users.append(user)
        print(f"Created user{i}")
    
    # Create sample blog posts
    posts = []
    for i in range(1, 6):
        user = users[(i-1) % len(users)]
        post = BlogPost.objects.create(
            title=f'Sample Blog Post {i}',
            content=f'This is the content of blog post {i}. It contains some sample text for demonstration purposes.\n\n'
                    f'This is a second paragraph of the blog post. It demonstrates how paragraphs work.',
            author=user,
            created_at=timezone.now()
        )
        posts.append(post)
        print(f"Created blog post {i}")
    
    # Create sample comments
    for i in range(1, 11):
        post = posts[(i-1) % len(posts)]
        user = users[i % len(users)]
        Comment.objects.create(
            post=post,
            author=user,
            content=f'This is comment {i} on the blog post. It adds some discussion value.',
            created_at=timezone.now()
        )
        print(f"Created comment {i}")
    
    # Add likes to posts
    for i, post in enumerate(posts):
        # Each post is liked by different users
        for j in range(len(users)):
            if i != j:  # User doesn't like their own post
                post.liked_by.add(users[j])
                print(f"Added like from user{j+1} to post {i+1}")
    
    print("Sample data creation complete!")

if __name__ == '__main__':
    # Use transaction to ensure all data is created or none
    with transaction.atomic():
        create_sample_data() 