# Generated by Django 2.1.5 on 2019-01-24 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workload', '0007_wallphotowrapper_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workload',
            name='status',
            field=models.IntegerField(choices=[(1, 'InitialUpload'), (2, 'FirstSketchesHaveAdded'), (3, 'SketchesBeenApprovedByCouncil'), (5, 'LegalAgreementIsReady'), (8, 'StreetArtIsComplete'), (13, 'StreetArtCorrespondsToAgreement')]),
        ),
    ]