# Generated by Django 3.2 on 2021-04-16 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock_management', '0002_stockhistory'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stockhistory',
            old_name='last_updated',
            new_name='last_update',
        ),
    ]
