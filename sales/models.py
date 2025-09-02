from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


class Sale(models.Model):
    """銷售額模型"""
    
    CATEGORY_CHOICES = [
        ('堂食', '堂食'),
        ('外帶', '外帶'),
        ('外送', '外送'),
        ('其他', '其他'),
    ]
    
    date = models.DateTimeField(
        verbose_name='日期時間',
        help_text='銷售日期時間'
    )
    
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='銷售金額',
        help_text='當日銷售總額'
    )
    
    description = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='說明',
        help_text='銷售情況說明'
    )
    
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='堂食',
        verbose_name='銷售類別'
    )
    
    store_id = models.CharField(
        max_length=50,
        default='main_store',
        verbose_name='店面ID',
        help_text='未來擴展多店管理用'
    )
    
    recorded_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='sales_recorded',
        verbose_name='記錄人員'
    )
    
    notes = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='備註',
        help_text='額外說明或備註'
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
        verbose_name = '銷售額'
        verbose_name_plural = '銷售額'
        ordering = ['-date', '-created_at']
        unique_together = ['date', 'store_id']  # 同店同日期只能有一筆記錄
        indexes = [
            models.Index(fields=['date', 'store_id']),
            models.Index(fields=['store_id', 'date']),
            models.Index(fields=['category', 'store_id']),
        ]
    
    def __str__(self):
        return f"{self.date} - {self.store_id} - ${self.amount}"
    
    @property
    def formatted_amount(self):
        """格式化金額"""
        return f"${self.amount:,.2f}"
    
    @property
    def category_display(self):
        """取得類別顯示名稱"""
        return self.get_category_display()
    
    def save(self, *args, **kwargs):
        """儲存時自動設定店面ID"""
        if not self.store_id:
            self.store_id = self.recorded_by.store_id
        super().save(*args, **kwargs)


class SaleCategory(models.Model):
    """銷售類別模型（可擴展）"""
    
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='類別名稱'
    )
    
    description = models.TextField(
        max_length=200,
        blank=True,
        verbose_name='類別說明'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='啟用狀態'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='建立時間'
    )
    
    class Meta:
        verbose_name = '銷售類別'
        verbose_name_plural = '銷售類別'
        ordering = ['name']
    
    def __str__(self):
        return self.name

