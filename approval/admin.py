from django.contrib import admin
from approval.models import SketchDecision, WallPhotoWrapperDecision, SketchVote

models_list = [SketchDecision, WallPhotoWrapperDecision, SketchVote]

admin.site.site_title = 'AnyArt site admin'
admin.site.site_url = 'https://anyart.netlify.com'
admin.site.site_header = 'AnyArt administration'
admin.site.register(models_list)