from django.db import migrations, models
from django.utils import timezone
from datetime import datetime, time

def convert_date_to_datetime(apps, schema_editor):
    """將現有的日期資料轉換為日期時間"""
    Sale = apps.get_model('sales', 'Sale')
    
    # 更新所有現有的銷售記錄，將日期設為當天的中午12點
    for sale in Sale.objects.all():
        if hasattr(sale, 'date') and sale.date:
            # 如果 date 是 DateField，轉換為 DateTimeField
            if isinstance(sale.date, datetime):
                # 已經是 datetime，不需要轉換
                continue
            else:
                # 將日期轉換為當天中午12點的 datetime
                sale.date = datetime.combine(sale.date, time(12, 0))
                sale.save()

def reverse_convert_date_to_datetime(apps, schema_editor):
    """反向轉換：將日期時間轉換回日期"""
    Sale = apps.get_model('sales', 'Sale')
    
    for sale in Sale.objects.all():
        if hasattr(sale, 'date') and sale.date:
            # 將 datetime 轉換為 date
            if isinstance(sale.date, datetime):
                sale.date = sale.date.date()
                sale.save()

class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        # 先轉換資料
        migrations.RunPython(convert_date_to_datetime, reverse_convert_date_to_datetime),
        
        # 然後修改欄位類型
        migrations.AlterField(
            model_name='sale',
            name='date',
            field=models.DateTimeField(
                verbose_name='日期時間',
                help_text='銷售日期時間'
            ),
        ),
    ]
