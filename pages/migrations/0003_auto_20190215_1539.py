

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_auto_20190214_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='Date_From',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 15, 15, 39, 38, 696062)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='Date_To',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 15, 15, 39, 38, 696062)),
        ),
        migrations.AlterField(
            model_name='car',
            name='Date_From',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 15, 15, 39, 38, 696062)),
        ),
        migrations.AlterField(
            model_name='car',
            name='Date_To',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 15, 15, 39, 38, 696062)),
        ),
        migrations.AlterField(
            model_name='parking',
            name='user_parking',
            field=models.ForeignKey(default=0, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_parking', to=settings.AUTH_USER_MODEL),
        ),
    ]
