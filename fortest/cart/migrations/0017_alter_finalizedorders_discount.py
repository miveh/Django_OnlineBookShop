# Generated by Django 3.2.6 on 2021-08-21 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0016_alter_finalizedorders_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finalizedorders',
            name='discount',
            field=models.IntegerField(default=0),
        ),
    ]
