# Generated by Django 2.0.2 on 2018-06-20 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jwt_auth', '0005_auto_20180417_0923'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EmailVerifycode',
        ),
        migrations.AlterField(
            model_name='staff',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='是否激活'),
        ),
    ]