from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models

# ensure unique email field
User._meta.get_field('email')._unique = True


class UserProfile(models.Model):
    BASIC = 'basic'
    ARTIST = 'artist'
    GOVERNMENT = 'gov'
    rights_types = [
        (BASIC, 'BasicUser'),
        (ARTIST, 'Artist'),
        (GOVERNMENT, 'GovernmentRepresentative')
    ]
    owner = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, blank=False, null=False,
                              related_name='user_profile')
    rights = models.CharField(blank=False, max_length=50, choices=rights_types)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        rights_list = [self.BASIC, self.ARTIST, self.GOVERNMENT]
        if self.rights in rights_list:
            super(UserProfile, self).save(*args, **kwargs)
        else:
            raise Exception("rights field can only take certain values: 'basic', 'artist', 'gov'")

    def __str__(self):
        return '%s: %s' % (self.owner.username, self.rights)


class BasicUserProfile(UserProfile):
    ...


class GovernmentUserProfile(UserProfile):
    # todo complete authority choices
    LCC = 'lcc'
    authority_choices = [
        (LCC, 'Lviv City Council')
    ]
    authority = models.CharField(blank=False, null=False, choices=authority_choices)

    def save(self, *args, **kwargs):
        rights_list = [self.BASIC, self.ARTIST, self.GOVERNMENT]
        authority_list = [self.LCC, ]
        if self.rights in rights_list and self.authority in authority_list:
            super(UserProfile, self).save(*args, **kwargs)
        else:
            raise Exception("rights field can only take certain values: 'basic', 'artist', 'gov'")


class ArtistUserProfile(UserProfile):
    ...