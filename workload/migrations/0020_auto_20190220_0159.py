# Generated by Django 2.1.5 on 2019-02-19 23:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workload', '0019_auto_20190216_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sketchimage',
            name='sketch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sketch_images', to='workload.Sketch'),
        ),
    ]
