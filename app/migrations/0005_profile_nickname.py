# Generated by Django 3.2.8 on 2021-12-28 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_anslike_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='nickname',
            field=models.CharField(default='', max_length=255),
        ),
    ]
