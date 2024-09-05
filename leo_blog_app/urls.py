from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('blogs/<str:user_name>/<int:blog_id>', views.blog_detail, name='blogdetail'),
    path('create_blog/', views.create_blog, name='create_blog'),
    path('blog/delete/<int:blog_id>/', views.delete_blog, name='delete_blog'),
    path('profile/<str:user_name>', views.profile, name='profile'), 
]