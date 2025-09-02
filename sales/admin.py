from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Sale, SaleCategory


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    """銷售額管理後台"""
    
    list_display = [
        'date', 'store_id', 'amount', 'category', 
        'recorded_by', 'description', 'created_at'
    ]
    
    list_filter = [
        'date', 'store_id', 'category', 'recorded_by',
        'created_at', 'updated_at'
    ]
    
    search_fields = [
        'description', 'notes', 'recorded_by__username',
        'recorded_by__first_name', 'recorded_by__last_name'
    ]
    
    list_per_page = 50
    date_hierarchy = 'date'
    
    fieldsets = (
        ('基本資訊', {
            'fields': ('date', 'amount', 'category', 'description')
        }),
        ('店面資訊', {
            'fields': ('store_id',)
        }),
        ('記錄資訊', {
            'fields': ('recorded_by', 'notes')
        }),
        ('時間資訊', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        """只顯示當前使用者有權限查看的銷售額"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(store_id=request.user.store_id)
    
    def save_model(self, request, obj, form, change):
        """儲存時自動設定記錄人員和店面ID"""
        if not change:  # 新增時
            obj.recorded_by = request.user
            obj.store_id = request.user.store_id
        super().save_model(request, obj, form, change)
    
    def formatted_amount_display(self, obj):
        """格式化金額顯示"""
        return format_html(
            '<span style="color: green; font-weight: bold;">{}</span>',
            obj.formatted_amount
        )
    formatted_amount_display.short_description = '金額'
    
    def get_list_display(self, request):
        """動態調整列表顯示欄位"""
        list_display = list(super().get_list_display(request))
        # 將金額欄位替換為格式化版本
        if 'amount' in list_display:
            list_display[list_display.index('amount')] = 'formatted_amount_display'
        return list_display


@admin.register(SaleCategory)
class SaleCategoryAdmin(admin.ModelAdmin):
    """銷售類別管理後台"""
    
    list_display = ['name', 'description', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']
    
    fieldsets = (
        ('基本資訊', {
            'fields': ('name', 'description')
        }),
        ('狀態', {
            'fields': ('is_active',)
        }),
        ('時間資訊', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at']

