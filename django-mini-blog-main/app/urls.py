from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('search/', views.search_posts, name='search_posts'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('clear-welcome-toast/', views.clear_welcome_toast, name='clear_welcome_toast'),
    path('blogs/', views.blog_list, name='blog_list'),
    path('blog/<int:post_id>/', views.blog_detail, name='blog_detail'),
    path('blog/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('blogger/<int:author_id>/', views.blogger_detail, name='blogger_detail'),
    path('author/<int:author_id>/', views.blogger_detail, name='author_detail'),
    path('bloggers/', views.blogger_list, name='blogger_list'),
    path('blog/<int:post_id>/like/', views.like_post, name='like_post'),
    path('blog/<int:post_id>/dislike/', views.dislike_post, name='dislike_post'),
    path('saved-posts/', views.saved_posts, name='saved_posts'),
    path('blog/<int:post_id>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('create-blog/', views.create_blog, name='create_blog'),
    # Special initialization endpoint
    path('init-database/', views.initialize_database, name='initialize_database'),
] 