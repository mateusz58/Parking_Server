# Generated by Django 2.0.13 on 2019-02-15 21:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_auto_20190215_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='Date_From',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 15, 22, 47, 41, 91987)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='Date_To',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 15, 22, 47, 41, 91987)),
        ),
        migrations.AlterField(
            model_name='car',
            name='Date_From',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 15, 22, 47, 41, 91987)),
        ),
        migrations.AlterField(
            model_name='car',
            name='Date_To',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 15, 22, 47, 41, 91987)),
        ),
    ]
