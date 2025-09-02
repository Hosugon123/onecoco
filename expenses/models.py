from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


class Expense(models.Model):
    """支出模型 - 用於記帳管理的日常支出"""
    
    CATEGORY_CHOICES = [
        ('日常支出', '日常支出'),
        ('食材採購', '食材採購'),
        ('水電費', '水電費'),
        ('租金', '租金'),
        ('人工費', '人工費'),
        ('其他', '其他'),
    ]
    
    date = models.DateTimeField(
        verbose_name='支出時間',
        help_text='支出發生的日期時間'
    )
    
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='支出金額',
        help_text='支出金額'
    )
    
    item_name = models.CharField(
        max_length=200,
        verbose_name='支出項目',
        help_text='支出項目名稱'
    )
    
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='日常支出',
        verbose_name='支出類別'
    )
    
    notes = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='備註',
        help_text='支出說明或備註'
    )
    
    recorded_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='expenses_recorded',
        verbose_name='記錄人員'
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
        verbose_name = '支出'
        verbose_name_plural = '支出'
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['category']),
            models.Index(fields=['recorded_by']),
        ]
    
    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d %H:%M')} - {self.item_name} - ${self.amount}"
    
    @property
    def formatted_amount(self):
        """格式化金額"""
        return f"${self.amount:,.2f}"
    
    @property
    def category_display(self):
        """取得類別顯示名稱"""
        return self.get_category_display()
