from django.contrib import admin
from . import models as m
models_list = [m.User, m.BasicUserProfile, m.ArtistUserProfile, m.GovernmentUserProfile]

admin.site.site_title = 'AnyArt site admin'
admin.site.site_url = 'https://anyart.netlify.com'
admin.site.site_header = 'AnyArt administration'
admin.site.register(models_list)
