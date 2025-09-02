from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = '詳細資料'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """自定義使用者管理後台"""
    
    inlines = (UserProfileInline,)
    
    list_display = (
        'username', 'email', 'first_name', 'last_name', 
        'role', 'store_id', 'is_active', 'date_joined'
    )
    
    list_filter = (
        'role', 'store_id', 'is_active', 'is_staff', 
        'is_superuser', 'date_joined'
    )
    
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('個人資訊'), {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        (_('權限'), {
            'fields': (
                'role', 'store_id', 'is_active', 'is_staff', 
                'is_superuser', 'groups', 'user_permissions'
            ),
        }),
        (_('重要日期'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'password1', 'password2', 'email',
                'first_name', 'last_name', 'role', 'store_id'
            ),
        }),
    )
    
    def get_queryset(self, request):
        """只顯示當前使用者有權限查看的使用者"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # 創始人只能看到同店的使用者
        return qs.filter(store_id=request.user.store_id)
    
    def save_model(self, request, obj, form, change):
        """儲存時自動設定店面ID"""
        if not change:  # 新增使用者時
            obj.store_id = request.user.store_id
        super().save_model(request, obj, form, change)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """使用者詳細資料管理後台"""
    
    list_display = ('user', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('user', 'avatar', 'bio')
        }),
        (_('時間資訊'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

