from django.db import models

rights_types = [
    ('basic', 'basic'),
    ('artist', 'artist'),
    ('gov', 'gov')
]


class UserProfile(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=False)
    rights = models.CharField(blank=False, max_length=50, choices=rights_types)