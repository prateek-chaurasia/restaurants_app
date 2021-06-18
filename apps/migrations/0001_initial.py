# Generated by Django 2.2 on 2021-06-17 09:59

import datetime
from django.conf import settings
import django.contrib.gis.geos.point
from django.db import migrations, models
import django.db.models.deletion
import location_field.models.spatial


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('address', models.TextField(blank=True, default='')),
                ('date', models.DateField(default=datetime.date.today)),
                ('location', location_field.models.spatial.LocationField(default=django.contrib.gis.geos.point.Point(1.0, 1.0), srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='RestaurantReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(choices=[(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four'), (5, 'five')], default=3, verbose_name='Rating (stars)')),
                ('comment', models.TextField(blank=True, null=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='apps.Restaurant')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MapUserRestaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suggested', models.BooleanField(default=False)),
                ('visited', models.BooleanField(default=False)),
                ('restaurant', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='apps.Restaurant')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
