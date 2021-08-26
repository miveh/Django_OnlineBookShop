# Generated by Django 3.2.6 on 2021-08-26 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartCoupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=30)),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('is_active', models.BooleanField(default=False)),
                ('discount_percent', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'تخفیف درصدی سبد',
                'verbose_name_plural': 'تخفیف درصدی سبدهای خریده',
            },
        ),
        migrations.CreateModel(
            name='BookPercentCoupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('is_active', models.BooleanField(default=False)),
                ('discount_percent', models.IntegerField(default=0)),
                ('books', models.ManyToManyField(blank=True, to='book.Book')),
            ],
            options={
                'verbose_name': 'تخفیف درصدی کتاب',
                'verbose_name_plural': 'تخفیف درصدی کتاب ها',
            },
        ),
        migrations.CreateModel(
            name='BookCashCoupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('is_active', models.BooleanField(default=False)),
                ('discount_price', models.IntegerField(default=0)),
                ('books', models.ManyToManyField(blank=True, to='book.Book')),
            ],
            options={
                'verbose_name': 'تخفیف نقدی کتاب',
                'verbose_name_plural': 'تخفیف نقدی کتاب ها',
            },
        ),
    ]
