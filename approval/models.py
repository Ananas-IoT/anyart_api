from django.contrib.auth import get_user_model
from django.db import models


class ApprovalGroup(models.Model):
    workload = models.ForeignKey('workload.Workload', on_delete=models.CASCADE, blank=False, null=False)
    approvers = models.ManyToManyField(get_user_model(), related_name='approval_groups')

    def __str__(self):
        return self.workload.__str__()


class GovDecision(models.Model):
    # vote choices
    DISAPPROVED = 0
    APPROVED = 1
    VETO = 13
    vote_choices = [
        (DISAPPROVED, "Disapproved"),
        (APPROVED, "Approved"),
        (VETO, "Veto")
    ]

    # group role choices
    TOURISM_MANAGEMENT = 'Tourism Management'
    IT_MANAGEMENT = 'IT management'
    HISTORY_PRESERVATION_MANAGEMENT = 'History Preservation Management'
    MAIN_ARCHITECT = 'Main Architect'
    OWNER = 'Owner'
    ART_EXPERT = 'Art Expert'
    group_role_choices = [
        (TOURISM_MANAGEMENT, 'Tourism Management'),
        (IT_MANAGEMENT, 'IT management'),
        (HISTORY_PRESERVATION_MANAGEMENT, 'History Preservation Management'),
        (MAIN_ARCHITECT, 'Main Architect'),
        (OWNER, 'Owner'),
        (ART_EXPERT, 'Art Expert')
    ]

    class Meta:
        abstract = True
        permissions = [
            ('can_approve_object', 'Can Approve Object'),
            ('can_disapprove_object', 'Can Disapprove Object'),
            ('can_veto_object', 'Can Veto Object')
        ]

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=False, null=False)
    group_role = models.CharField(max_length=100, choices=group_role_choices, blank=False, null=False)
    approval_group = models.ForeignKey('approval.ApprovalGroup', on_delete=models.CASCADE, blank=False, null=False)
    vote = models.IntegerField(choices=vote_choices, null=True)

    def save(self, *args, **kwargs):
        vote_list = [choice[0] for choice in self.vote_choices]
        group_role_list = [choice[0] for choice in self.group_role_choices]
        if self.vote in vote_list and self.group_role in group_role_list:
            super().save(*args, **kwargs)
        else:
            raise Exception("vote or group_role field is invalid")

    def __str__(self):
        return f"{self.owner.__str__()}:{self.group_role}"


class SketchDecision(GovDecision):
    sketch = models.ForeignKey('workload.Sketch', on_delete=models.CASCADE, blank=False, null=False)


class WallPhotoWrapperDecision(GovDecision):
    wall_photo_wrapper = models.ForeignKey('workload.WallPhotoWrapper', on_delete=models.CASCADE,
                                           blank=False, null=False)


class SketchVote(models.Model):
    LIKE = 1
    DISLIKE = 0
    user_vote_choices = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike')
    ]
    sketch = models.ForeignKey('workload.Sketch', on_delete=models.CASCADE, blank=False, null=False)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=False, null=False)
    vote = models.IntegerField(choices=user_vote_choices, blank=False, null=False)
    created_at = models.DateTimeField(auto_now=True)
