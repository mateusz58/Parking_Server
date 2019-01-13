# Generated by Django 2.1.4 on 2019-01-13 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('code', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('registration_plate', models.CharField(max_length=20)),
                ('Date_From', models.DateTimeField()),
                ('Date_To', models.DateTimeField()),
                ('Cost', models.FloatField(default=0)),
                ('status', models.CharField(choices=[('ACTIVE', 'active'), ('EXPIRED', 'expired')], default='ACTIVE', editable=False, max_length=1)),
                ('active', models.BooleanField(default=True, editable=False)),
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
                ('free_places', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='parking',
            unique_together={('x', 'y')},
        ),
        migrations.AddField(
            model_name='booking',
            name='parking',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parking', to='pages.Parking'),
        ),
    ]
