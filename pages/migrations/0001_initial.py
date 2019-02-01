# Generated by Django 2.1.4 on 2019-02-01 16:53

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('code', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('registration_plate', models.CharField(max_length=20)),
                ('Date_From', models.DateTimeField(default=datetime.datetime(2019, 2, 1, 17, 53, 12, 887667))),
                ('Date_To', models.DateTimeField(default=datetime.datetime(2019, 2, 1, 17, 53, 12, 887667))),
                ('Cost', models.FloatField(default=0)),
                ('status', models.CharField(choices=[('ACTIVE', 'active'), ('EXPIRED', 'expired'), ('RESERVED', 'reserved'), ('CANCELLED', 'cancelled')], default='ACTIVE', max_length=1)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Parking',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('parking_name', models.CharField(max_length=200, unique=True)),
                ('parking_Street', models.CharField(max_length=200)),
                ('parking_City', models.CharField(max_length=200)),
                ('x', models.FloatField(default=0)),
                ('y', models.FloatField(default=0)),
                ('number_of_places', models.PositiveIntegerField(default=1)),
                ('free_places', models.PositiveIntegerField(default=models.PositiveIntegerField(default=1))),
                ('HOUR_COST', models.FloatField(default=2.0)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='parking',
            unique_together={('parking_Street', 'parking_City')},
        ),
        migrations.AddField(
            model_name='booking',
            name='parking',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parking', to='pages.Parking'),
        ),
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
