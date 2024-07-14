# Generated by Django 5.0.6 on 2024-07-14 18:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentPlan',
            fields=[
                ('id', models.BigIntegerField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('price', models.PositiveIntegerField(null=True)),
                ('price_type', models.CharField(choices=[('week', 'Week'), ('month', 'Month'), ('free', 'Free')], default='free', max_length=10)),
                ('trial_days', models.PositiveIntegerField(blank=True, null=True)),
                ('trial_discount_percent', models.PositiveIntegerField(blank=True, null=True)),
                ('banner', models.ImageField(upload_to='banners/')),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=10)),
                ('description', models.TextField(max_length=250)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'content plan',
                'verbose_name_plural': 'content plans',
                'db_table': 'content_plan',
                'ordering': ('-created_at',),
            },
        ),
    ]
