# Generated by Django 5.0.3 on 2024-03-19 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0003_computer_created_at_computer_created_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='computer',
            name='warranty_info',
            field=models.CharField(default='N/A', max_length=100, verbose_name='Warranty'),
        ),
    ]
