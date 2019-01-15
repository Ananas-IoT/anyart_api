from django.db import models

# Create your models here.


class UserProfile(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=False)
    rights = models.CharField(blank=False, max_length=50)