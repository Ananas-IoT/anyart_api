from django.contrib.auth import get_user_model
from django.db import models


class ApprovalGroup(models.Model):
    workload = models.ForeignKey('workload.Workload', on_delete=models.CASCADE)
    approvers = models.ManyToManyField(get_user_model(), related_name='approval_groups')

    def __str__(self):
        return self.workload.__str__()


class GovDecision(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    group_role = models.CharField(max_length=100)
    vote = models.IntegerField()

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.owner.__str__()}:{self.group_role}"


class SketchDecision(GovDecision):
    sketch = models.ForeignKey('workload.Sketch', on_delete=models.CASCADE)


class WallPhotoWrapperDecision(GovDecision):
    wall_photo_wrapper = models.ForeignKey('workload.WallPhotoWrapper', on_delete=models.CASCADE)