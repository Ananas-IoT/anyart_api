from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models


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

    TOURISM_MANAGEMENT = 'tourism_management'
    IT_MANAGEMENT = 'it_management'
    HISTORY_PRESERVATION_MANAGEMENT = 'history_preservation_management'
    MAIN_ARCHITECT = 'main_architect'
    OWNER = 'owner'
    ART_EXPERT = 'art_expert'
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
            ('can_veto', 'Can Veto Object')
        ]

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    group_role = models.ForeignKey('auth.Group', on_delete=models.CASCADE)
    vote = models.IntegerField(choices=vote_choices, null=True)
    voted_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        vote_list = [choice[0] for choice in self.vote_choices]
        vote_list.append(None)
        if self.vote in vote_list:
            super().save(*args, **kwargs)
        else:
            raise Exception("vote or group_role field is invalid")

    def __str__(self):
        return f"{self.owner.__str__()}:{self.group_role}"


class SketchDecision(GovDecision):
    sketch = models.ForeignKey('workload.Sketch', on_delete=models.CASCADE, blank=False, null=False,
                               related_name='decisions')


class WallPhotoWrapperDecision(GovDecision):
    wall_photo_wrapper = models.ForeignKey('workload.WallPhotoWrapper', on_delete=models.CASCADE,
                                           blank=False, null=False, related_name='decisions')


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