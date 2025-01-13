# Generated by Django 5.1.4 on 2025-01-13 17:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_roles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.BigIntegerField(db_index=True, unique=True, verbose_name='telegram|model|telegram_chat|chat_id')),
                ('username', models.CharField(blank=True, max_length=64, null=True, verbose_name='telegram|model|telegram_chat|username')),
                ('title', models.CharField(max_length=64, verbose_name='telegram|model|telegram_chat|title')),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'Telegram|model|telegram_chat|chat_type|private'), (2, 'Telegram|model|telegram_chat|chat_type|group')], verbose_name='Telegram|model|telegram_chat|type')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='telegram|model|telegram_chat|created_at')),
                ('role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user_roles.userrole', verbose_name='Telegram|model|telegram_chat|role')),
            ],
            options={
                'verbose_name': 'telegram|model|telegram_chat',
                'verbose_name_plural': 'telegram|model|telegram_chats',
            },
        ),
    ]
