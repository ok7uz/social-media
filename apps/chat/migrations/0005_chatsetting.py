# Generated by Django 5.0.6 on 2024-08-09 11:54

import config.utils
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_messageread'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatSetting',
            fields=[
                ('id', config.utils.CustomAutoField(editable=False, primary_key=True, serialize=False)),
                ('message_first_permission', models.CharField(choices=[('superhero', 'Superhero'), ('nobody', 'Nobody')], default='superhero', max_length=10)),
                ('response_permissions', models.JSONField(default={'follower': True, 'subscriber': True, 'superhero': True})),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='chat_settings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'chat setting',
                'verbose_name_plural': 'chat settings',
                'db_table': 'chat_settings',
                'ordering': ('created_at',),
            },
        ),
    ]
