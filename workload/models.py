import boto3
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models
from django.dispatch import receiver
from anyart_api import settings
from anyart_api import storage_backends as sb
from approval.models import WallPhotoWrapperDecision


class Workload(models.Model):
    JUST_CREATED = 1
    SKETCHES_ADDED = 2
    SKETCHES_APPROVED = 3
    AGREEMENT_READY = 5
    ART_READY = 8
    ART_APPROVED = 13

    status_choices = [
        (JUST_CREATED, 'InitialUpload'),
        (SKETCHES_ADDED, 'FirstSketchesHaveAdded'),
        (SKETCHES_APPROVED, 'SketchesBeenApprovedByCouncil'),
        (AGREEMENT_READY, 'LegalAgreementIsReady'),
        (ART_READY, 'StreetArtIsComplete'),
        (ART_APPROVED, 'StreetArtCorrespondsToAgreement')
    ]
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=True)
    status = models.IntegerField(null=False, blank=True, choices=status_choices, default=JUST_CREATED)
    requirements = models.TextField(null=True, blank=True)

    def __str__(self):
        return 'initialized by %s, %s' % (self.created_at.date(), self.created_at.time())


class Sketch(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=False)
    workload = models.ForeignKey('workload.Workload', on_delete=models.CASCADE, blank=False, null=False)
    sketch_description = models.TextField(blank=True, null=False, default='Not provided')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = "sketches"

    def __str__(self):
        return 'owner: %s: workload_id: %s' % (self.owner.username, self.workload_id)


class Location(models.Model):
    street_address = models.CharField(max_length=200, blank=True, null=True)
    lng = models.FloatField(blank=False, null=False)
    lat = models.FloatField(blank=False, null=False)

    def __str__(self):
        return '%s, lng: %s, lat: %s' % (self.street_address or 'Unknown address', self.lng, self.lat)


class Limitation(models.Model):
    location = models.ForeignKey('workload.Location', on_delete=models.CASCADE, related_name='limitation',
                                    blank=True, null=False)
    authority = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='limitation_authority',
                                  blank=True, null=False)
    reason = models.TextField(max_length=500, blank=False, null=False)


class WallPhotoWrapper(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='photo_wrappers',
                              blank=True, null=False)
    workload = models.OneToOneField('workload.Workload', on_delete=models.CASCADE, related_name='wall_photo_wrapper',
                                    blank=False, null=False)
    location = models.OneToOneField('workload.Location', on_delete=models.CASCADE, related_name='photo_wrapper',
                                    blank=False, null=False)
    description = models.TextField(blank=True, null=False, default='Not provided')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return '%s:%s' % (self.owner, self.description[:50])


class Restriction(models.Model):
    """The most mysterious class in AnyArt"""
    location = models.ForeignKey('workload.Location', on_delete=models.CASCADE, blank=False, null=False)


"""---------------------------------------------------FILES------------------------------------------------------"""


class AbstractFile(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        abstract = True


class WallPhoto(AbstractFile):
    wrapper = models.ForeignKey('workload.WallPhotoWrapper', on_delete=models.CASCADE,
                                related_name='wall_photos', blank=False, null=False)
    photo = models.ImageField(storage=sb.PublicMediaStorage(), upload_to='wall_photos',
                              blank=False, null=False)

    def __str__(self):
        return 'wrapper: %s, photo: %s' % (self.wrapper_id, self.photo)

    @receiver(models.signals.post_delete, sender='workload.WallPhoto')
    def delete_static_on_delete(sender, instance, using, **kwargs):
        s3 = boto3.resource('s3')
        s3.Object(f'{settings.AWS_STORAGE_BUCKET_NAME}',
                  '%s/%s' % (settings.AWS_PUBLIC_MEDIA_LOCATION, str(instance.photo))).delete()

    # @receiver(models.signals.pre_save, sender='workload.WallPhoto')
    # def delete_static_on_change(sender, instance, using, **kwargs):
    #     try:
    #         old = WallPhoto.objects.get(pk=instance.pk)
    #     except WallPhoto.DoesNotExist:
    #         return None
    #     s3 = boto3.resource('s3')
    #     s3.Object(f'{settings.AWS_STORAGE_BUCKET_NAME}',
    #               '%s/%s' % (settings.AWS_PUBLIC_MEDIA_LOCATION, str(old.photo))).delete()


class SketchImage(AbstractFile):
    sketch = models.ForeignKey('workload.Sketch', on_delete=models.CASCADE, blank=False, null=False,
                               related_name='sketch_images')
    image = models.FileField(storage=sb.PublicMediaStorage(), upload_to='sketches',
                             blank=False, null=False)

    @receiver(models.signals.post_delete, sender='workload.SketchImage')
    def delete_static_on_delete(sender, instance, using, **kwargs):
        s3 = boto3.resource('s3')
        s3.Object(f'{settings.AWS_STORAGE_BUCKET_NAME}',
                  '%s/%s' % (settings.AWS_PUBLIC_MEDIA_LOCATION, str(instance.image))).delete()

    # @receiver(models.signals.pre_save, sender='workload.SketchImage')
    # def delete_static_on_change(sender, instance, using, **kwargs):
    #     try:
    #         old = WallPhoto.objects.get(pk=instance.pk)
    #     except WallPhoto.DoesNotExist:
    #         return None
    #     s3 = boto3.resource('s3')
    #     s3.Object(f'{settings.AWS_STORAGE_BUCKET_NAME}',
    #               '%s/%s' % (settings.AWS_PUBLIC_MEDIA_LOCATION, str(old.photo))).delete()


class PhotoAfter(AbstractFile):
    workload = models.ForeignKey('workload.Workload', on_delete=models.CASCADE, blank=False, null=False,
                                 related_name='after_photos')
    photo = models.ImageField(storage=sb.PublicMediaStorage(), upload_to='after_photos',
                              blank=False, null=False)


class LegalAgreement(AbstractFile):
    workload = models.ForeignKey('workload.Workload', on_delete=models.CASCADE, blank=False, null=False)
    file = models.FileField(storage=sb.PrivateMediaStorage(), upload_to='legal_agreements',
                            blank=False, null=False)


class PermissionLetter(AbstractFile):
    workload = models.ForeignKey('workload.Workload', on_delete=models.CASCADE, blank=False, null=False)
    file = models.FileField(storage=sb.PrivateMediaStorage(), upload_to='permission_letters',
                            blank=False, null=False)
