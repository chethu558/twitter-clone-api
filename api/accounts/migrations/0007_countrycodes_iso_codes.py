# Generated by Django 2.2.17 on 2021-03-07 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20210307_0359'),
    ]

    operations = [
        migrations.AddField(
            model_name='countrycodes',
            name='iso_codes',
            field=models.CharField(default='IN', max_length=10),
        ),
    ]
