# Generated by Django 4.2.1 on 2023-05-12 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_ash', '0002_emailverifyrecordash_alter_userprofileash_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofileash',
            name='desc',
            field=models.TextField(blank=True, default='', max_length=200, verbose_name='个人简介'),
        ),
        migrations.AddField(
            model_name='userprofileash',
            name='gexing',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='个性签名'),
        ),
    ]
