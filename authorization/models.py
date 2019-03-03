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
    rights = models.CharField(blank=False, max_length=50, choices=rights_types)

    def save(self, *args, **kwargs):
        rights_list = [self.BASIC, self.ARTIST, self.GOVERNMENT]
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
    # todo complete authority choices
    LCC = 'lcc'
    authority_choices = [
        (LCC, 'Lviv City Council')
    ]

    authority = models.CharField(max_length=100, blank=False, null=False, choices=authority_choices)
    owner = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, blank=False, null=False,
                                 related_name='gov_user_profile')

    def save(self, *args, **kwargs):
        rights_list = [self.BASIC, self.ARTIST, self.GOVERNMENT]
        authority_list = [self.LCC, ]
        if self.rights in rights_list and self.authority in authority_list:
            super(UserProfile, self).save(*args, **kwargs)
        else:
            raise Exception("rights field can only take certain values: 'basic', 'artist', 'gov'")


class ArtistUserProfile(UserProfile):
    owner = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, blank=False, null=False,
                                 related_name='artist_user_profile')