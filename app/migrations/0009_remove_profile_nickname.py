# Generated by Django 3.2.10 on 2022-01-15 22:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_tag_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='nickname',
        ),
    ]