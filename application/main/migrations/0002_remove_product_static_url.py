# Generated by Django 3.1.7 on 2021-04-09 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='static_url',
        ),
    ]
