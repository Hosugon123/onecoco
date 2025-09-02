from django.db import migrations, models
from django.utils import timezone
from datetime import datetime, time

def convert_date_to_datetime(apps, schema_editor):
    """將現有的日期資料轉換為日期時間"""
    Cost = apps.get_model('costs', 'Cost')
    
    # 更新所有現有的成本記錄，將日期設為當天的中午12點
    for cost in Cost.objects.all():
        if hasattr(cost, 'date') and cost.date:
            # 如果 date 是 DateField，轉換為 DateTimeField
            if isinstance(cost.date, datetime):
                # 已經是 datetime，不需要轉換
                continue
            else:
                # 將日期轉換為當天中午12點的 datetime
                cost.date = datetime.combine(cost.date, time(12, 0))
                cost.save()

def reverse_convert_date_to_datetime(apps, schema_editor):
    """反向轉換：將日期時間轉換回日期"""
    Cost = apps.get_model('costs', 'Cost')
    
    for cost in Cost.objects.all():
        if hasattr(cost, 'date') and cost.date:
            # 將 datetime 轉換為 date
            if isinstance(cost.date, datetime):
                cost.date = cost.date.date()
                cost.save()

class Migration(migrations.Migration):

    dependencies = [
        ('costs', '0001_initial'),
    ]

    operations = [
        # 先轉換資料
        migrations.RunPython(convert_date_to_datetime, reverse_convert_date_to_datetime),
        
        # 然後修改欄位類型
        migrations.AlterField(
            model_name='cost',
            name='date',
            field=models.DateTimeField(
                verbose_name='日期時間',
                help_text='成本發生日期時間'
            ),
        ),
    ]
