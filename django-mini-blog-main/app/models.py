from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

class UserManager(BaseUserManager):
    def create_user(self, username, email, full_name=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            full_name=full_name or username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, full_name=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, full_name or username, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(username=username)

class User(AbstractUser):
    full_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(max_length=200, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bookmarks = models.ManyToManyField('BlogPost', related_name='bookmarked_by', blank=True)

    objects = UserManager()

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    liked_by = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    disliked_by = models.ManyToManyField(User, related_name='disliked_posts', blank=True)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.liked_by.count() - self.disliked_by.count()

    def is_liked_by(self, user):
        return self.liked_by.filter(id=user.id).exists()

    def is_disliked_by(self, user):
        return self.disliked_by.filter(id=user.id).exists()

    def like(self, user):
        if not self.is_liked_by(user):
            self.liked_by.add(user)
            if self.is_disliked_by(user):
                self.disliked_by.remove(user)
            self.save()
            return True
        return False

    def dislike(self, user):
        if not self.is_disliked_by(user):
            self.disliked_by.add(user)
            if self.is_liked_by(user):
                self.liked_by.remove(user)
            self.save()
            return True
        return False

    def unlike(self, user):
        if self.is_liked_by(user):
            self.liked_by.remove(user)
            self.save()
            return True
        return False

    def undislike(self, user):
        if self.is_disliked_by(user):
            self.disliked_by.remove(user)
            self.save()
            return True
        return False

    class Meta:
        ordering = ['-created_at']

class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
