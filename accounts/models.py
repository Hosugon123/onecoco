from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """自定義使用者模型"""
    
    ROLE_CHOICES = [
        ('founder', '創始人'),
        ('franchisee', '加盟商'),
        ('staff', '員工'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='founder',
        verbose_name='角色'
    )
    
    store_id = models.CharField(
        max_length=50,
        default='main_store',
        verbose_name='店面ID'
    )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='電話'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='啟用狀態'
    )
    
    last_login_ip = models.GenericIPAddressField(
        blank=True,
        null=True,
        verbose_name='最後登入IP'
    )
    
    class Meta:
        verbose_name = '使用者'
        verbose_name_plural = '使用者'
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"
    
    @property
    def is_founder(self):
        return self.role == 'founder'
    
    @property
    def is_franchisee(self):
        return self.role == 'franchisee'
    
    @property
    def is_staff_member(self):
        return self.role == 'staff'


class UserProfile(models.Model):
    """使用者詳細資料"""
    
    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='使用者'
    )
    
    avatar = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='頭像路徑',
        help_text='頭像檔案路徑'
    )
    
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='個人簡介'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='建立時間'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新時間'
    )
    
    class Meta:
        verbose_name = '使用者詳細資料'
        verbose_name_plural = '使用者詳細資料'
    
    def __str__(self):
        return f"{self.user.username} 的詳細資料"

