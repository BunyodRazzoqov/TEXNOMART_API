# Generated by Django 5.1.2 on 2024-10-16 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texnomart', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='group',
            new_name='category',
        ),
    ]
