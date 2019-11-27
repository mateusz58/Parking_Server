

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20190215_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='Date_From',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 15, 18, 26, 36, 767490)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='Date_To',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 15, 18, 26, 36, 768488)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='car',
            name='Date_From',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 15, 18, 26, 36, 768488)),
        ),
        migrations.AlterField(
            model_name='car',
            name='Date_To',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 15, 18, 26, 36, 768488)),
        ),
    ]
