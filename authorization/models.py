from django.contrib.auth import get_user_model
from django.db import models

rights_types = [
    ('basic', 'basic'),
    ('artist', 'artist'),
    ('gov', 'gov')
]


class UserProfile(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=False, null=False)
    rights = models.CharField(blank=False, max_length=50, choices=rights_types)