# Generated by Django 3.2.6 on 2021-08-21 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0008_auto_20210814_1740'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='discount',
        ),
    ]
