

import datetime
from django.conf import settings
import django.core.validators
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
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('Cost', models.FloatField(default=0, editable=False)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('number_of_cars', models.PositiveIntegerField(default=0)),
                ('Date_From', models.DateTimeField(default=datetime.datetime(2019, 2, 14, 13, 32, 9, 413365))),
                ('Date_To', models.DateTimeField(default=datetime.datetime(2019, 2, 14, 13, 32, 9, 413365))),
                ('active', models.BooleanField(default=True, editable=False)),
                ('created_by', models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modified_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('Date_From', models.DateTimeField(default=datetime.datetime(2019, 2, 14, 13, 32, 9, 414362))),
                ('Date_To', models.DateTimeField(default=datetime.datetime(2019, 2, 14, 13, 32, 9, 414362))),
                ('registration_plate', models.CharField(default='default', max_length=10, validators=[django.core.validators.RegexValidator('^[\\w]*$', code='Invalid name', message='name must be alphanumeric')])),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('EXPIRED', 'Expired'), ('RESERVED', 'Reserved'), ('CANCELLED', 'Cancelled'), ('RESERVED_L', 'Reserved Late'), ('EXPIRED_E', 'Expired early')], default='ACTIVE', max_length=10)),
                ('Cost', models.FloatField(default=0, editable=False)),
                ('booking', models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='booking', to='pages.Booking')),
            ],
        ),
        migrations.CreateModel(
            name='Parking',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('parking_name', models.CharField(max_length=30, unique=True)),
                ('parking_Street', models.CharField(max_length=20)),
                ('parking_City', models.CharField(max_length=20)),
                ('x', models.FloatField(default=0)),
                ('y', models.FloatField(default=0)),
                ('number_of_places', models.PositiveIntegerField(default=1)),
                ('free_places', models.PositiveIntegerField(default=0, editable=False)),
                ('HOUR_COST', models.FloatField(default=2.0)),
                ('user_parking', models.ForeignKey(default=0, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_parking', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='parking',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parking', to='pages.Parking'),
        ),
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='parking',
            unique_together={('parking_Street', 'parking_City')},
        ),
    ]
