# Generated by Django 2.0.2 on 2018-04-17 01:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jwt_auth', '0004_auto_20180416_1007'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EmailVericode',
            new_name='EmailVerifycode',
        ),
    ]