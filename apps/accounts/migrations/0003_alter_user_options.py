# Generated by Django 5.0.6 on 2024-08-10 10:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('first_name',), 'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
    ]
