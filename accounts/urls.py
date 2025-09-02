from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # 認證相關
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/profile/', views.user_profile, name='profile'),
    path('auth/profile/update/', views.update_profile, name='update_profile'),
    path('auth/change-password/', views.change_password, name='change_password'),
    
    # 使用者管理
    path('users/', views.UserListCreateView.as_view(), name='user_list_create'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    
    # 管理功能
    path('create-default-founders/', views.create_default_founders, name='create_default_founders'),
]

