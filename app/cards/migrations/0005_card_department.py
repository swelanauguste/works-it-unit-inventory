# Generated by Django 5.0.3 on 2024-05-07 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0004_card_is_printed_alter_card_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='department',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
