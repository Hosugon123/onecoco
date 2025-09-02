from django.db import models
from django.utils.translation import gettext_lazy as _


class Report(models.Model):
    """報表模型"""
    
    REPORT_TYPE_CHOICES = [
        ('daily', '日報'),
        ('weekly', '週報'),
        ('monthly', '月報'),
        ('quarterly', '季報'),
        ('yearly', '年報'),
        ('custom', '自定義'),
    ]
    
    name = models.CharField(
        max_length=100,
        verbose_name='報表名稱'
    )
    
    report_type = models.CharField(
        max_length=20,
        choices=REPORT_TYPE_CHOICES,
        default='daily',
        verbose_name='報表類型'
    )
    
    start_date = models.DateField(
        verbose_name='開始日期'
    )
    
    end_date = models.DateField(
        verbose_name='結束日期'
    )
    
    store_id = models.CharField(
        max_length=50,
        default='main_store',
        verbose_name='店面ID'
    )
    
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='reports_created',
        verbose_name='建立人員'
    )
    
    total_sales = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='總銷售額'
    )
    
    total_costs = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='總成本'
    )
    
    net_profit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='淨利潤'
    )
    
    profit_margin = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name='利潤率(%)'
    )
    
    notes = models.TextField(
        max_length=1000,
        blank=True,
        verbose_name='報表備註'
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
        verbose_name = '報表'
        verbose_name_plural = '報表'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['store_id', 'report_type']),
            models.Index(fields=['start_date', 'end_date']),
            models.Index(fields=['created_by', 'store_id']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.start_date} - {self.end_date})"
    
    @property
    def formatted_total_sales(self):
        """格式化總銷售額"""
        return f"${self.total_sales:,.2f}"
    
    @property
    def formatted_total_costs(self):
        """格式化總成本"""
        return f"${self.total_costs:,.2f}"
    
    @property
    def formatted_net_profit(self):
        """格式化淨利潤"""
        return f"${self.net_profit:,.2f}"
    
    @property
    def formatted_profit_margin(self):
        """格式化利潤率"""
        return f"{self.profit_margin:.2f}%"
    
    def calculate_profit_margin(self):
        """計算利潤率"""
        if self.total_sales > 0:
            self.profit_margin = (self.net_profit / self.total_sales) * 100
        else:
            self.profit_margin = 0
    
    def save(self, *args, **kwargs):
        """儲存時自動計算利潤率"""
        self.calculate_profit_margin()
        super().save(*args, **kwargs)


class ReportTemplate(models.Model):
    """報表模板模型"""
    
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='模板名稱'
    )
    
    description = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='模板說明'
    )
    
    template_type = models.CharField(
        max_length=20,
        choices=Report.REPORT_TYPE_CHOICES,
        verbose_name='模板類型'
    )
    
    is_default = models.BooleanField(
        default=False,
        verbose_name='是否為預設模板'
    )
    
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='templates_created',
        verbose_name='建立人員'
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
        verbose_name = '報表模板'
        verbose_name_plural = '報表模板'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """儲存時確保只有一個預設模板"""
        if self.is_default:
            ReportTemplate.objects.filter(
                template_type=self.template_type
            ).update(is_default=False)
        super().save(*args, **kwargs)

