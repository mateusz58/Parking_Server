

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='Date_From',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 14, 15, 21, 5, 553819)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='Date_To',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 14, 15, 21, 5, 553819)),
        ),
        migrations.AlterField(
            model_name='car',
            name='Date_From',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 14, 15, 21, 5, 554821)),
        ),
        migrations.AlterField(
            model_name='car',
            name='Date_To',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 14, 15, 21, 5, 554821)),
        ),
    ]
