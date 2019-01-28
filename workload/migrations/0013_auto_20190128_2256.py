# Generated by Django 2.1.5 on 2019-01-28 20:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workload', '0012_auto_20190125_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='street_address',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='wallphotowrapper',
            name='description',
            field=models.TextField(blank=True, default='Not provided'),
        ),
        migrations.AlterField(
            model_name='wallphotowrapper',
            name='location',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='photo_wrappers', to='workload.Location'),
        ),
        migrations.AlterField(
            model_name='wallphotowrapper',
            name='owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='photo_wrappers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='wallphotowrapper',
            name='workload',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photo_wrappers', to='workload.Workload'),
        ),
    ]
