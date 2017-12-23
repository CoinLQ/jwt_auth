# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-23 07:19
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('username', models.CharField(default='', max_length=24, verbose_name='用户名')),
                ('email', models.EmailField(db_index=True, max_length=255, unique=True, verbose_name='邮件')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否激活')),
                ('is_admin', models.BooleanField(default=False)),
                ('introduce_by', models.CharField(default='', max_length=64, verbose_name='推荐由')),
                ('date_joined', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
