from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('clear-welcome-toast/', views.clear_welcome_toast, name='clear_welcome_toast'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<int:post_id>/', views.blog_detail, name='blog_detail'),
    path('blog/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('author/<int:author_id>/', views.author_detail, name='author_detail'),
    path('blogger/<int:author_id>/', views.blogger_detail, name='blogger_detail'),
    path('bloggers/', views.blogger_list, name='blogger_list'),
    path('blog/<int:post_id>/like/', views.like_post, name='like_post'),
    path('blog/<int:post_id>/dislike/', views.dislike_post, name='dislike_post'),
    path('search/', views.search_posts, name='search_posts'),
] 