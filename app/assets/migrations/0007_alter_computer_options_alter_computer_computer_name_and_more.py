# Generated by Django 5.0.3 on 2024-05-18 18:12

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0006_alter_microsoftoffice_date_installed'),
        ('clients', '0003_alter_client_created_at_alter_client_updated_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='computer',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterField(
            model_name='computer',
            name='computer_name',
            field=models.CharField(blank=True, default='MCWT', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='computer',
            name='date_received',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='computer',
            name='department',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='computer_departments', to='clients.department'),
        ),
        migrations.AlterField(
            model_name='computer',
            name='location',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='computer_locations', to='assets.location'),
        ),
        migrations.AlterField(
            model_name='computer',
            name='status',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='assets.status'),
        ),
    ]
