from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models

# ensure unique email field
User._meta.get_field('email')._unique = True

class UserProfile(models.Model):
    BASIC = 'bas'
    ARTIST = 'art'
    GOVERNMENT = 'gov'
    rights_types = [
        (BASIC, 'BasicUser'),
        (ARTIST, 'Artist'),
        (GOVERNMENT, 'GovernmentRepresentative')
    ]
    owner = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, blank=False, null=False,
                              related_name='user_profile')
    rights = models.CharField(blank=False, max_length=50, choices=rights_types)

    def __str__(self):
        return '%s: %s' % (self.owner.username, self.rights)