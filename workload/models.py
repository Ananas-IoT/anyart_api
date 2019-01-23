from django.contrib.auth import get_user_model
from django.db import models
from anyart_api import storage_backends as sb


class Workload(models.Model):
    status = models.IntegerField(null=False, blank=False)
    requirements = models.TextField(null=True, blank=True)


class Sketch(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=False, null=False)
    workload = models.ForeignKey('workload.Workload', on_delete=models.CASCADE, blank=False, null=False)


class WallPhotoWrapper(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=False, null=False)
    workload = models.ForeignKey('workload.Workload', on_delete=models.CASCADE, blank=False, null=False)


class Location(models.Model):
    street_address = models.CharField(max_length=200, blank=True, null=True)
    lng = models.FloatField(blank=False, null=False)
    lat = models.FloatField(blank=False, null=False)


class Restriction(models.Model):
    """The most mysterious class in AnyArt"""
    location = models.ForeignKey('workload.Location', on_delete=models.CASCADE, blank=False, null=False)


"""
All models below represent files which will be stored in separate db tables.
File models should always extend AbstractFile models for convenience and scalability
"""
class AbstractFile(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        abstract = True


class WallPhoto(AbstractFile):
    wrapper = models.ForeignKey('workload.WallPhotoWrapper', on_delete=models.CASCADE,
                                blank=False, null=False)
    photo = models.ImageField(storage=sb.PublicMediaStorage(), upload_to='wall_photos',
                              blank=False, null=False)


class SketchImage(AbstractFile):
    sketch = models.ForeignKey('workload.Sketch', on_delete=models.CASCADE, blank=False, null=False)
    image = models.FileField(storage=sb.PublicMediaStorage(), upload_to='sketches',
                             blank=False, null=False)


class PhotoAfter(AbstractFile):
    workload = models.ForeignKey('workload.Workload', on_delete=models.CASCADE, blank=False, null=False)
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


# Sample Model for S3
class Document(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    upload = models.FileField(storage=sb.PrivateMediaStorage(), upload_to='documents')

