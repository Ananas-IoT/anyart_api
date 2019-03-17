from django.contrib.auth import get_user_model
from django.db import models


class ApprovalGroup(models.Model):
    workload = models.ForeignKey('workload.Workload', on_delete=models.CASCADE)
    approvers = models.ManyToManyField(get_user_model(), related_name='approval_groups')

    def __str__(self):
        return self.workload.__str__()


class GovDecision(models.Model):
    DISAPPROVED = 0
    APPROVED = 1
    VETO = 13
    vote_choices = [
        (DISAPPROVED, "Disapproved"),
        (APPROVED, "Approved"),
        (VETO, "Veto")
    ]

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    group_role = models.CharField(max_length=100)
    vote = models.IntegerField(choices=vote_choices)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.owner.__str__()}:{self.group_role}"


class SketchDecision(GovDecision):
    sketch = models.ForeignKey('workload.Sketch', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        vote_list = [self.BASIC, self.ARTIST, self.GOVERNMENT]
        if self.vote in vote_list:
            super(SketchDecision, self).save(*args, **kwargs)
        else:
            raise Exception("vote field can only take certain values: 0, 1, 13")


class WallPhotoWrapperDecision(GovDecision):
    wall_photo_wrapper = models.ForeignKey('workload.WallPhotoWrapper', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        vote_list = [self.BASIC, self.ARTIST, self.GOVERNMENT]
        if self.vote in vote_list:
            super(WallPhotoWrapperDecision, self).save(*args, **kwargs)
        else:
            raise Exception("vote field can only take certain values: 0, 1, 13")


class SketchVote(models.Model):
    sketch = models.ForeignKey('workload.Sketch', on_delete=models.CASCADE, blank=False, null=False)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=False, null=False)
    vote = models.IntegerField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now=True)
