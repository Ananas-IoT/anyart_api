# Generated by Django 2.1.5 on 2019-04-11 11:50

import anyart_api.storage_backends
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
            name='LegalAgreement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(storage=anyart_api.storage_backends.PrivateMediaStorage(), upload_to='legal_agreements')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.CharField(blank=True, max_length=200)),
                ('lng', models.FloatField()),
                ('lat', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='PermissionLetter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(storage=anyart_api.storage_backends.PrivateMediaStorage(), upload_to='permission_letters')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PhotoAfter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('photo', models.ImageField(storage=anyart_api.storage_backends.PublicMediaStorage(), upload_to='after_photos')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Restriction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workload.Location')),
            ],
        ),
        migrations.CreateModel(
            name='Sketch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sketch_description', models.TextField(blank=True, default='Not provided')),
                ('owner', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'sketches',
            },
        ),
        migrations.CreateModel(
            name='SketchImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('image', models.FileField(storage=anyart_api.storage_backends.PublicMediaStorage(), upload_to='sketches')),
                ('sketch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sketch_images', to='workload.Sketch')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WallPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('photo', models.ImageField(storage=anyart_api.storage_backends.PublicMediaStorage(), upload_to='wall_photos')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WallPhotoWrapper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, default='Not provided')),
                ('location', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='photo_wrapper', to='workload.Location')),
                ('owner', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='photo_wrappers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Workload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(blank=True, choices=[(1, 'InitialUpload'), (2, 'FirstSketchesHaveAdded'), (3, 'SketchesBeenApprovedByCouncil'), (5, 'LegalAgreementIsReady'), (8, 'StreetArtIsComplete'), (13, 'StreetArtCorrespondsToAgreement')], default=1)),
                ('requirements', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='wallphotowrapper',
            name='workload',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wall_photo_wrapper', to='workload.Workload'),
        ),
        migrations.AddField(
            model_name='wallphoto',
            name='wrapper',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wall_photos', to='workload.WallPhotoWrapper'),
        ),
        migrations.AddField(
            model_name='sketch',
            name='workload',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workload.Workload'),
        ),
        migrations.AddField(
            model_name='photoafter',
            name='workload',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='after_photos', to='workload.Workload'),
        ),
        migrations.AddField(
            model_name='permissionletter',
            name='workload',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workload.Workload'),
        ),
        migrations.AddField(
            model_name='legalagreement',
            name='workload',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workload.Workload'),
        ),
    ]
