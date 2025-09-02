from django.contrib import admin
from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['date', 'item_name', 'category', 'amount', 'recorded_by', 'created_at']
    list_filter = ['category', 'date', 'recorded_by']
    search_fields = ['item_name', 'notes']
    date_hierarchy = 'date'
    ordering = ['-date', '-created_at']
    
    fieldsets = (
        ('基本資訊', {
            'fields': ('date', 'item_name', 'amount', 'category')
        }),
        ('詳細資訊', {
            'fields': ('notes', 'recorded_by')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # 如果是新增
            obj.recorded_by = request.user
        super().save_model(request, obj, form, change)
