# Generated by Django 2.0.2 on 2018-06-15 02:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('jwt_auth', '0007_auto_20180612_0832'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailVerifycode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, verbose_name='验证码')),
                ('email', models.EmailField(max_length=50, verbose_name='邮箱')),
                ('send_type', models.CharField(choices=[('register', '注册'), ('forget', '找回密码')], max_length=10, verbose_name='验证码类型')),
                ('send_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='发送时间')),
            ],
            options={
                'verbose_name': '邮箱验证码',
                'verbose_name_plural': '邮箱验证码',
            },
        ),
        migrations.AlterField(
            model_name='staff',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='是否激活'),
        ),
    ]