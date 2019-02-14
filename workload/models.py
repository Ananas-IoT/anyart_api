from django.contrib.auth import get_user_model
from django.db import models

from anyart_api import storage_backends as sb


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
    created = models.DateTimeField(auto_now_add=True, null=False, blank=True)
    status = models.IntegerField(null=False, blank=True, choices=status_choices, default=JUST_CREATED)
    requirements = models.TextField(null=True, blank=True)


class Sketch(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=False)
    workload = models.ForeignKey('workload.Workload', on_delete=models.CASCADE, blank=False, null=False)


class Location(models.Model):
    street_address = models.CharField(max_length=200, blank=True, null=False)
    lng = models.FloatField(blank=False, null=False)
    lat = models.FloatField(blank=False, null=False)


class WallPhotoWrapper(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='photo_wrappers',
                              blank=True, null=False)
    workload = models.ForeignKey('workload.Workload', on_delete=models.CASCADE, related_name='photo_wrappers',
                                 blank=False, null=False)
    location = models.OneToOneField('workload.Location', on_delete=models.CASCADE, related_name='photo_wrappers',
                                 blank=False, null=False)
    description = models.TextField(blank=True, null=False, default='Not provided')


class Restriction(models.Model):
    """The most mysterious class in AnyArt"""
    location = models.ForeignKey('workload.Location', on_delete=models.CASCADE, blank=False, null=False)


"""------------------------------------------------------FILES-------------------------------------------------------"""


class AbstractFile(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        abstract = True


class WallPhoto(AbstractFile):
    wrapper = models.ForeignKey('workload.WallPhotoWrapper', on_delete=models.CASCADE,
                                related_name='wall_photos', blank=False, null=False)
    photo = models.ImageField(storage=sb.PublicMediaStorage(), upload_to='wall_photos',
                              blank=False, null=False)


class SketchImage(AbstractFile):
    sketch = models.ForeignKey('workload.Sketch', on_delete=models.CASCADE, blank=False, null=False,
                               related_name='sketches')
    image = models.FileField(storage=sb.PublicMediaStorage(), upload_to='sketches',
                             blank=False, null=False)


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