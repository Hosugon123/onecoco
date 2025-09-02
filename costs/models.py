from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


class Cost(models.Model):
    """成本模型"""
    
    CATEGORY_CHOICES = [
        ('食材', '食材'),
        ('營運費用', '營運費用'),
        ('人工', '人工'),
        ('水電', '水電'),
        ('租金', '租金'),
        ('其他', '其他'),
    ]
    
    date = models.DateTimeField(
        verbose_name='日期時間',
        help_text='成本發生日期時間'
    )
    
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='成本',
        help_text='成本'
    )
    
    description = models.CharField(
        max_length=200,
        verbose_name='說明',
        help_text='成本項目說明'
    )
    
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='食材',
        verbose_name='成本類別'
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
        related_name='costs_recorded',
        verbose_name='記錄人員'
    )
    
    supplier = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='供應商',
        help_text='供應商名稱'
    )
    
    invoice_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='發票號碼',
        help_text='發票或收據號碼'
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
        verbose_name = '成本'
        verbose_name_plural = '成本'
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['date', 'store_id']),
            models.Index(fields=['store_id', 'date']),
            models.Index(fields=['category', 'store_id']),
            models.Index(fields=['supplier', 'store_id']),
        ]
    
    def __str__(self):
        return f"{self.date} - {self.category} - {self.description} - ${self.amount}"
    
    @property
    def formatted_amount(self):
        """格式化成本"""
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


class CostCategory(models.Model):
    """成本類別模型（可擴展）"""
    
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
        verbose_name = '成本類別'
        verbose_name_plural = '成本類別'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Supplier(models.Model):
    """供應商模型"""
    
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='供應商名稱'
    )
    
    contact_person = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='聯絡人'
    )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='電話'
    )
    
    email = models.EmailField(
        blank=True,
        verbose_name='電子郵件'
    )
    
    address = models.TextField(
        max_length=200,
        blank=True,
        verbose_name='地址'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='啟用狀態'
    )
    
    notes = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='備註'
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
        verbose_name = '供應商'
        verbose_name_plural = '供應商'
        ordering = ['name']
    
    def __str__(self):
        return self.name

