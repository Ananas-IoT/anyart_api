from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    BASIC = 'basic'
    ARTIST = 'artist'
    GOVERNMENT = 'gov'
    rights_types = [
        (BASIC, 'BasicUser'),
        (ARTIST, 'Artist'),
        (GOVERNMENT, 'GovernmentRepresentative')
    ]

    email = models.EmailField('email address', blank=True, unique=True)
    rights = models.CharField(blank=False, max_length=50, choices=rights_types, default=BASIC)

    def save(self, *args, **kwargs):
        rights_list = [choice[0] for choice in self.rights_types]
        if self.rights in rights_list:
            super(User, self).save(*args, **kwargs)
        else:
            raise Exception("rights field can only take certain values: 'basic', 'artist', 'gov'")


class UserProfile(models.Model):

    class Meta:
        abstract = True

    def __str__(self):
        return '%s' % self.owner.username


class BasicUserProfile(UserProfile):
    owner = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, blank=False, null=False,
                                 related_name='basic_user_profile')


class GovernmentUserProfile(UserProfile):
    CULTURE_MANAGEMENT = 'culture_management'
    TOURISM_MANAGEMENT = 'tourism_management'
    IT_MANAGEMENT = 'it_management'
    HISTORY_PRESERVATION_MANAGEMENT = 'history_preservation_management'
    MAIN_ARCHITECT = 'main_architect'

    authority_choices = [
        (CULTURE_MANAGEMENT, 'Culture Management'),
        (TOURISM_MANAGEMENT, 'Tourism Management'),
        (IT_MANAGEMENT, 'IT management'),
        (HISTORY_PRESERVATION_MANAGEMENT, 'History Preservation Management'),
        (MAIN_ARCHITECT, 'Main Architect')
    ]

    authority = models.CharField(max_length=100, blank=False, null=False,
                                 choices=authority_choices, default=IT_MANAGEMENT)
    owner = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, blank=False, null=False,
                                 related_name='gov_user_profile')

    def save(self, *args, **kwargs):
        authority_list = [choice[0] for choice in self.authority_choices]
        if self.authority in authority_list:
            super(UserProfile, self).save(*args, **kwargs)
        else:
            raise Exception("authority choices must be only of certain types")


class ArtistUserProfile(UserProfile):
    owner = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, blank=False, null=False,
                                 related_name='artist_user_profile')


