# Generated by Django 2.1.5 on 2019-01-24 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workload', '0009_auto_20190124_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workload',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]