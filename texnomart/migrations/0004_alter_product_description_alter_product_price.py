# Generated by Django 5.1.2 on 2024-10-16 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('texnomart', '0003_rename_group_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, default='good', null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
