# Generated by Django 5.0.3 on 2024-03-26 17:15

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_rename_role_licence_rename_cat_card_licence'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name'], 'verbose_name_plural': 'categories'},
        ),
        migrations.AddField(
            model_name='card',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='card',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='licence_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='card',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='card',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='licence_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='card',
            name='expires',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='licence_no',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AlterField(
            model_name='card',
            name='photo',
            field=models.FileField(blank=True, upload_to='photos'),
        ),
        migrations.AlterField(
            model_name='card',
            name='signature',
            field=models.FileField(blank=True, upload_to='signatures'),
        ),
    ]
