# Generated by Django 2.0.5 on 2018-06-14 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('jwt_auth', '0005_auto_20180417_0923'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='username',
            field=models.CharField(db_index=True, default='', max_length=24, unique=True, verbose_name='用户名'),
        ),
    ]
