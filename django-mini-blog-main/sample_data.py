from django.contrib.auth import get_user_model
from app.models import BlogPost, Comment
from django.utils import timezone

User = get_user_model()

def create_sample_data():
    # Get or create admin user
    admin_user = User.objects.get(username='admin')
    
    # Create sample blog posts
    posts = [
        {
            'title': 'Welcome to Django Mini Blog',
            'content': '''Welcome to our Django Mini Blog! This is a simple yet powerful blogging platform built with Django.
            
Here you can share your thoughts, ideas, and experiences with the world. The platform supports markdown formatting, comments, and a like/dislike system.

Feel free to explore and engage with other bloggers in our community!''',
        },
        {
            'title': 'Getting Started with Django',
            'content': '''Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design.
            
Here are some key features of Django:
- Built-in admin interface
- Object-relational mapper (ORM)
- URL routing
- Template engine
- Form handling
- Authentication system

If you're new to Django, check out the official documentation at https://docs.djangoproject.com/''',
        },
        {
            'title': 'Web Development Best Practices',
            'content': '''When developing web applications, it's important to follow these best practices:

1. Write Clean Code
   - Follow PEP 8 style guide for Python
   - Use meaningful variable and function names
   - Keep functions small and focused

2. Security First
   - Always validate user input
   - Use HTTPS
   - Keep dependencies updated
   - Hash passwords properly

3. Performance Matters
   - Optimize database queries
   - Use caching when appropriate
   - Minimize HTTP requests
   - Compress static files''',
        }
    ]
    
    # Create blog posts
    for post_data in posts:
        post = BlogPost.objects.create(
            title=post_data['title'],
            content=post_data['content'],
            author=admin_user,
            created_at=timezone.now()
        )
        print(f"Created blog post: {post.title}")

if __name__ == '__main__':
    create_sample_data() 