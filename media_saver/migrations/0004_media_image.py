# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-11-27 19:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_saver', '0003_auto_20171127_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='image',
            field=models.ImageField(default='pic_folder/None/no-img.jpg', upload_to='pic_folder/'),
        ),
    ]
