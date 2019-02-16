from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    BASIC = 'bas'
    ARTIST = 'art'
    GOVERNMENT = 'gov'
    rights_types = [
        (BASIC, 'BasicUser'),
        (ARTIST, 'Artist'),
        (GOVERNMENT, 'GovernmentRepresentative')
    ]
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=False, null=False)
    rights = models.CharField(blank=False, max_length=50, choices=rights_types)

    def __str__(self):
        return self.user.username