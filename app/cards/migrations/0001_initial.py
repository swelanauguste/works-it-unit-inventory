# Generated by Django 5.0.3 on 2024-03-26 12:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.FileField(upload_to='photos')),
                ('name', models.CharField(max_length=200)),
                ('licence_no', models.CharField(max_length=5)),
                ('expires', models.DateField()),
                ('signature', models.FileField(upload_to='signatures')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.category')),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.role')),
            ],
        ),
    ]
