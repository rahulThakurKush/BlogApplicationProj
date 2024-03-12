from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # This maps the root URL to the index view
    path('signup/', views.signup, name='signup'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('login/', views.user_login, name='user_login'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('my_blogs',views.my_blogs, name='my_blogs'),
    path('blogs/', views.show_blog, name='show_blog'),
    path('post_detail/<int:pk>/', views.post_detail, name='post_detail'),
    path('like/<int:pk>/', views.like_post, name= 'like_post'),
    path('dislike/<int:pk>/', views.dislike_post, name= 'dislike_post'),
    path('category_detail/<int:pk>/',views.category_detail, name='category_detail'),
]
