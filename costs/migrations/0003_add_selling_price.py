# Generated manually

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('costs', '0002_convert_date_to_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='cost',
            name='selling_price',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text='商品售價（可選）',
                max_digits=10,
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name='售價'
            ),
        ),
    ]
